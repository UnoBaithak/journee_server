from __future__ import annotations

import copy
import uuid
from datetime import datetime
from typing import Any, Optional

from google.adk.events import Event
from google.adk.sessions import BaseSessionService, Session, State, _session_util
from google.adk.sessions.base_session_service import GetSessionConfig, ListSessionsResponse
import logging
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConfigurationError, ConnectionFailure
from tzlocal import get_localzone

logger = logging.getLogger(__name__)


class MongoSessionService(BaseSessionService):
    """A session service that uses MongoDB for storage."""

    def __init__(self, mongo_url: str, database_name: str = "journee", **kwargs: Any):
        """Initializes the MongoDB session service with a connection URL and
        database name."""
        try:
            self.client = MongoClient(mongo_url, **kwargs)
            # Test the connection
            self.client.admin.command("ping")
        except ConnectionFailure as e:
            logger.exception("Failed to connect to MongoDB")
            raise ValueError(f"Failed to connect to MongoDB at '{mongo_url}'") from e
        except ConfigurationError as e:
            logger.exception("MongoDB configuration error")
            raise ValueError(f"Invalid MongoDB configuration for URL '{mongo_url}'") from e
        except Exception as e:
            logger.exception("Unexpected error connecting to MongoDB")
            raise ValueError(f"Failed to create MongoDB client for URL '{mongo_url}'") from e

        # Get the local timezone
        local_timezone = get_localzone()
        logger.info(f"Local timezone: {local_timezone}")

        self.db: Database = self.client[database_name]

        # Collections
        self.sessions_collection: Collection = self.db.sessions
        self.events_collection: Collection = self.db.events
        self.app_states_collection: Collection = self.db.app_states
        self.user_states_collection: Collection = self.db.user_states

        # Create indexes for better performance
        # self._create_indexes()

    def _create_indexes(self):
        """Create necessary indexes for optimal performance."""
        # Sessions collection indexes
        self.sessions_collection.create_index(
            [("app_name", 1), ("user_id", 1), ("id", 1)], unique=True
        )
        self.sessions_collection.create_index(
            [("app_name", 1), ("user_id", 1), ("update_time", -1)]
        )

        # Events collection indexes
        self.events_collection.create_index(
            [("app_name", 1), ("user_id", 1), ("session_id", 1), ("id", 1)], unique=True
        )
        self.events_collection.create_index([("session_id", 1), ("timestamp", -1)])

        # App states collection indexes
        self.app_states_collection.create_index("app_name", unique=True)

        # User states collection indexes
        self.user_states_collection.create_index([("app_name", 1), ("user_id", 1)], unique=True)

    async def create_session(
        self,
        *,
        app_name: str,
        user_id: str,
        state: Optional[dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> Session:
        """Create a new session in MongoDB."""

        # Generate session ID if not provided
        if session_id is None:
            session_id = str(uuid.uuid4())

        current_time = datetime.utcnow()

        # Fetch app and user states from storage
        app_state_doc = self.app_states_collection.find_one({"app_name": app_name})
        user_state_doc = self.user_states_collection.find_one(
            {"app_name": app_name, "user_id": user_id}
        )

        app_state = app_state_doc.get("state", {}) if app_state_doc else {}
        user_state = user_state_doc.get("state", {}) if user_state_doc else {}

        # Create state documents if they don't exist
        if not app_state_doc:
            self.app_states_collection.insert_one(
                {"app_name": app_name, "state": {}, "update_time": current_time}
            )

        if not user_state_doc:
            self.user_states_collection.insert_one(
                {"app_name": app_name, "user_id": user_id, "state": {}, "update_time": current_time}
            )

        # Extract state deltas
        app_state_delta, user_state_delta, session_state = _extract_state_delta(state)

        # Apply state delta
        app_state.update(app_state_delta)
        user_state.update(user_state_delta)

        # Update app and user state if there are changes
        if app_state_delta:
            self.app_states_collection.update_one(
                {"app_name": app_name}, {"$set": {"state": app_state, "update_time": current_time}}
            )

        if user_state_delta:
            self.user_states_collection.update_one(
                {"app_name": app_name, "user_id": user_id},
                {"$set": {"state": user_state, "update_time": current_time}},
            )

        # Create the session document
        session_doc = {
            "app_name": app_name,
            "user_id": user_id,
            "id": session_id,
            "state": session_state,
            "create_time": current_time,
            "update_time": current_time,
        }

        self.sessions_collection.insert_one(session_doc)

        # Merge states for response
        merged_state = _merge_state(app_state, user_state, session_state)

        return Session(
            app_name=app_name,
            user_id=user_id,
            id=session_id,
            state=merged_state,
            last_update_time=current_time.timestamp(),
        )

    async def get_session(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        config: Optional[GetSessionConfig] = None,
    ) -> Optional[Session]:
        """Retrieve a session from MongoDB."""

        # Get the session document
        session_doc = self.sessions_collection.find_one(
            {"app_name": app_name, "user_id": user_id, "id": session_id}
        )

        if session_doc is None:
            return None

        # Build event query filters
        event_filter = {"session_id": session_id, "app_name": app_name, "user_id": user_id}

        if config and config.after_timestamp:
            after_dt = datetime.fromtimestamp(config.after_timestamp)
            event_filter["timestamp"] = {"$gte": after_dt}

        # Query events with sorting and limiting
        events_cursor = self.events_collection.find(event_filter).sort("timestamp", -1)

        if config and config.num_recent_events:
            events_cursor = events_cursor.limit(config.num_recent_events)

        event_docs = list(events_cursor)

        # Fetch states from storage
        app_state_doc = self.app_states_collection.find_one({"app_name": app_name})
        user_state_doc = self.user_states_collection.find_one(
            {"app_name": app_name, "user_id": user_id}
        )

        app_state = app_state_doc.get("state", {}) if app_state_doc else {}
        user_state = user_state_doc.get("state", {}) if user_state_doc else {}
        session_state = session_doc.get("state", {})

        # Merge states
        merged_state = _merge_state(app_state, user_state, session_state)

        # Convert to Session object
        session = Session(
            app_name=app_name,
            user_id=user_id,
            id=session_id,
            state=merged_state,
            last_update_time=session_doc["update_time"].timestamp(),
        )

        # Convert event documents to Event objects (reverse order since we sorted desc)
        session.events = [self._doc_to_event(doc) for doc in reversed(event_docs)]

        return session

    async def list_sessions(self, *, app_name: str, user_id: str) -> ListSessionsResponse:
        """List all sessions for a given app and user."""

        session_docs = self.sessions_collection.find(
            {"app_name": app_name, "user_id": user_id}
        ).sort("update_time", -1)

        sessions = []
        for doc in session_docs:
            session = Session(
                app_name=app_name,
                user_id=user_id,
                id=doc["id"],
                state={},
                last_update_time=doc["update_time"].timestamp(),
            )
            sessions.append(session)

        return ListSessionsResponse(sessions=sessions)

    async def delete_session(self, app_name: str, user_id: str, session_id: str) -> None:
        """Delete a session and all its events."""

        # Delete the session (events will be deleted via cascade in relational DB,
        # but in MongoDB we need to delete them explicitly)
        self.sessions_collection.delete_one(
            {"app_name": app_name, "user_id": user_id, "id": session_id}
        )

        # Delete all events for this session
        self.events_collection.delete_many(
            {"app_name": app_name, "user_id": user_id, "session_id": session_id}
        )

    async def append_event(self, session: Session, event: Event) -> Event:
        """Append an event to a session."""
        # logger.info(f"Append event: {event} to session {session.id}")

        if event.partial:
            return event

        # Get current session document to check for stale timestamps
        session_doc = self.sessions_collection.find_one(
            {"app_name": session.app_name, "user_id": session.user_id, "id": session.id}
        )

        if not session_doc:
            raise ValueError(f"Session not found: {session.id}")

        if session_doc["update_time"].timestamp() > session.last_update_time:
            raise ValueError(
                "The last_update_time provided in the session object"
                f" {datetime.fromtimestamp(session.last_update_time):'%Y-%m-%d %H:%M:%S'} is"
                " earlier than the update_time in the storage_session"
                f" {session_doc['update_time']:'%Y-%m-%d %H:%M:%S'}. Please check"
                " if it is a stale session."
            )

        current_time = datetime.utcnow()

        # Fetch states from storage
        app_state_doc = self.app_states_collection.find_one({"app_name": session.app_name})
        user_state_doc = self.user_states_collection.find_one(
            {"app_name": session.app_name, "user_id": session.user_id}
        )

        app_state = app_state_doc.get("state", {}) if app_state_doc else {}
        user_state = user_state_doc.get("state", {}) if user_state_doc else {}
        session_state = session_doc.get("state", {})

        # Extract state delta from event actions
        app_state_delta = {}
        user_state_delta = {}
        session_state_delta = {}

        if event.actions and event.actions.state_delta:
            app_state_delta, user_state_delta, session_state_delta = _extract_state_delta(
                event.actions.state_delta
            )

        # Update states if there are changes
        if app_state_delta:
            app_state.update(app_state_delta)
            self.app_states_collection.update_one(
                {"app_name": session.app_name},
                {"$set": {"state": app_state, "update_time": current_time}},
            )

        if user_state_delta:
            user_state.update(user_state_delta)
            self.user_states_collection.update_one(
                {"app_name": session.app_name, "user_id": session.user_id},
                {"$set": {"state": user_state, "update_time": current_time}},
            )

        if session_state_delta:
            session_state.update(session_state_delta)
            self.sessions_collection.update_one(
                {"app_name": session.app_name, "user_id": session.user_id, "id": session.id},
                {"$set": {"state": session_state, "update_time": current_time}},
            )

        # Insert the event document
        event_doc = self._event_to_doc(session, event)
        self.events_collection.insert_one(event_doc)

        # Update session timestamp
        session.last_update_time = current_time.timestamp()

        # Also update the in-memory session
        await super().append_event(session=session, event=event)
        return event

    def _event_to_doc(self, session: Session, event: Event) -> dict[str, Any]:
        """Convert an Event object to a MongoDB document."""
        doc = {
            "id": event.id,
            "app_name": session.app_name,
            "user_id": session.user_id,
            "session_id": session.id,
            "invocation_id": event.invocation_id,
            "author": event.author,
            "branch": event.branch,
            "timestamp": datetime.fromtimestamp(event.timestamp),
            "long_running_tool_ids": list(event.long_running_tool_ids)
            if event.long_running_tool_ids
            else [],
            "partial": event.partial,
            "turn_complete": event.turn_complete,
            "error_code": event.error_code,
            "error_message": event.error_message,
            "interrupted": event.interrupted,
        }

        # Serialize actions to dict if present
        if event.actions:
            if hasattr(event.actions, "model_dump"):
                # If it's a Pydantic model
                doc["actions"] = event.actions.model_dump(exclude_none=True, mode="json")
            elif hasattr(event.actions, "__dict__"):
                # If it's a regular Python object, convert to dict
                doc["actions"] = self._serialize_object(event.actions)
            else:
                # If it's already serializable
                doc["actions"] = event.actions
        else:
            doc["actions"] = None

        if event.content:
            doc["content"] = event.content.model_dump(exclude_none=True, mode="json")

        if event.grounding_metadata:
            doc["grounding_metadata"] = event.grounding_metadata.model_dump(
                exclude_none=True, mode="json"
            )

        return doc

    def _doc_to_event(self, doc: dict[str, Any]) -> Event:
        """Convert a MongoDB document to an Event object."""
        # Deserialize actions from dict if present
        actions = None
        if doc.get("actions"):
            actions = self._deserialize_actions(doc["actions"])

        return Event(
            id=doc["id"],
            invocation_id=doc["invocation_id"],
            author=doc["author"],
            branch=doc.get("branch"),
            actions=actions,
            timestamp=doc["timestamp"].timestamp(),
            content=_session_util.decode_content(doc.get("content")),
            long_running_tool_ids=set(doc.get("long_running_tool_ids", [])),
            partial=doc.get("partial"),
            turn_complete=doc.get("turn_complete"),
            error_code=doc.get("error_code"),
            error_message=doc.get("error_message"),
            interrupted=doc.get("interrupted"),
            grounding_metadata=_session_util.decode_grounding_metadata(
                doc.get("grounding_metadata")
            ),
        )

    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()

    def _serialize_object(self, obj: Any) -> dict[str, Any]:
        """Serialize a Python object to a dictionary for MongoDB storage."""
        if hasattr(obj, "model_dump"):
            # Pydantic model
            return obj.model_dump(exclude_none=True, mode="json")
        elif hasattr(obj, "__dict__"):
            # Regular Python object
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith("_"):  # Skip private attributes
                    if hasattr(value, "model_dump"):
                        result[key] = value.model_dump(exclude_none=True, mode="json")
                    elif hasattr(value, "__dict__"):
                        result[key] = self._serialize_object(value)
                    elif isinstance(value, (list, tuple)):
                        result[key] = [
                            self._serialize_object(item) if hasattr(item, "__dict__") else item
                            for item in value
                        ]
                    elif isinstance(value, dict):
                        result[key] = {
                            k: self._serialize_object(v) if hasattr(v, "__dict__") else v
                            for k, v in value.items()
                        }
                    else:
                        result[key] = value
            return result
        else:
            return obj

    def _deserialize_actions(self, actions_dict: dict[str, Any]) -> Any:
        """Deserialize actions dictionary back to the appropriate object.

        This is a simple implementation that returns the dict as-is. You
        may need to customize this based on your EventActions class
        structure.
        """
        # Since the original SQLAlchemy version stores actions using PickleType,
        # and we're now using JSON serialization, we need to handle the deserialization.
        # The exact implementation depends on how your EventActions class is structured.

        # For now, we'll return the dictionary as-is since most of the code
        # should work with dictionary access patterns.
        # If you need to reconstruct the actual EventActions object, you'll need to
        # import the class and reconstruct it:

        # Example (uncomment and modify based on your actual EventActions class):
        # from ..events.event_actions import EventActions
        # return EventActions(**actions_dict)

        return actions_dict


def _extract_state_delta(state: dict[str, Any]):
    """Extract state deltas for app, user, and session scopes."""
    app_state_delta = {}
    user_state_delta = {}
    session_state_delta = {}

    if state:
        for key in state.keys():
            if key.startswith(State.APP_PREFIX):
                app_state_delta[key.removeprefix(State.APP_PREFIX)] = state[key]
            elif key.startswith(State.USER_PREFIX):
                user_state_delta[key.removeprefix(State.USER_PREFIX)] = state[key]
            elif not key.startswith(State.TEMP_PREFIX):
                session_state_delta[key] = state[key]

    return app_state_delta, user_state_delta, session_state_delta


def _merge_state(app_state, user_state, session_state):
    """Merge app, user, and session states into a single state dictionary."""
    merged_state = copy.deepcopy(session_state)

    for key in app_state.keys():
        merged_state[State.APP_PREFIX + key] = app_state[key]

    for key in user_state.keys():
        merged_state[State.USER_PREFIX + key] = user_state[key]

    return merged_state
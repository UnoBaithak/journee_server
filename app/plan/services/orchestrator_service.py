from pydantic import BaseModel

from conversations.services import ConversationService
from itinerary.services import ItineraryService
from itinerary.models import Itinerary
from plan.models.request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from llm import LLMService
from enum import Enum
from users.services import UserInternalService
from hotspots import HotspotService
import logging

logger = logging.getLogger("uvicorn")

class OrchestratorContext(str, Enum):
    GENERATE = "Generate"
    UPDATE_FULL = "UpdateFull"
    UPDATE_DAY = "UpdateDay"


class Orchestrator:
    """Orchestrator for the whole of Athena"""

    def __init__(self):
        self.conversation_service = ConversationService()
        self.itinerary_service = ItineraryService()
        self.llm_service = LLMService()
        self.user_service = UserInternalService()
        self.hotspots_service = HotspotService()

    async def handle(self, model: BaseModel, request_context: OrchestratorContext):
        if request_context == OrchestratorContext.GENERATE:
            return await self._handle_itinerary_generation(model)
        elif request_context == OrchestratorContext.UPDATE_DAY:
            return await self._handle_day_update(model)
        elif request_context == OrchestratorContext.UPDATE_FULL:
            return await self._handle_full_itinerary_update(model)
        else:
            raise RuntimeError("Unknown context : {}", request_context)

    async def _handle_itinerary_generation(self, itineraryGenerationRequestModel: ItineraryGenerationRequestModel):
        logger.info("Create a new conversation")
        conversation_id = self.conversation_service.create_conversation()

        logger.info("Generate itinerary from LLM")
        itinerary: Itinerary = self.llm_service.chat(conversation_id, str(itineraryGenerationRequestModel))
        logger.info(f"Link itinerary with conversation id")
        itinerary.metadata.conversationId = conversation_id
        
        logger.info(f"Update conversation {conversation_id} with user and llm messages")
        self.conversation_service.add_message_to_converstion(conversation_id, str(itineraryGenerationRequestModel), "user")
        self.conversation_service.add_message_to_converstion(conversation_id, message_text=itinerary.model_dump(), role="assistant")

        logger.info("Populate hotspot metadata for itinerary")
        await self.hotspots_service.populate_hotspot_metadata(itinerary)

        logger.info("Link itinerary creatorId and userId if userId is available")
        if itineraryGenerationRequestModel.user_id is not None:
            itinerary.metadata.creatorId = itineraryGenerationRequestModel.user_id
            
        logger.info("Save itinerary to DB")
        itinerary_id = self.itinerary_service.create_new_itinerary(itinerary)

        if itineraryGenerationRequestModel.user_id is not None:
            logger.info("Add itinerary to list of draft itineraries")
            self.user_service.add_draft_itinerary(itinerary_id, itineraryGenerationRequestModel.user_id)
        
        return {"itinerary_id": itinerary_id}


    async def _handle_full_itinerary_update(self, itineraryUpdationRequestModel: ItineraryUpdationRequestModel):
        conversation_id = self.itinerary_service.get_itinerary(itineraryUpdationRequestModel.itinerary_id)["metadata"]["conversationId"]

        logger.info("Generate updated itinerary")
        updated_itinerary = self.llm_service.chat(conversation_id, itineraryUpdationRequestModel.user_input)
        logger.info("Update hotspot metadata")
        await self.hotspots_service.populate_hotspot_metadata(updated_itinerary)
        logger.info(f"Update the original itinerary in DB")
        self.itinerary_service.update_itinerary(itineraryUpdationRequestModel.itinerary_id, updated_itinerary)

        logger.info(f"Add user and assistant messages to conversation")
        self.conversation_service.add_message_to_converstion(conversation_id, itineraryUpdationRequestModel.user_input, "user")
        self.conversation_service.add_message_to_converstion(conversation_id, updated_itinerary.model_dump(), "assistant")


    async def _handle_day_update(self, itineraryUpdationRequestModel: ItineraryUpdationRequestModel):
        pass


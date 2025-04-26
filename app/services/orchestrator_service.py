from pydantic import BaseModel

from conversations import ConversationService
from itinerary import ItineraryService
from request_models.itinerary_request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from llm import LLMService
from enum import Enum
from users.user_service import UserService

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
        self.user_service = UserService()

    async def handle(self, model: BaseModel, request_context: OrchestratorContext):
        if request_context == OrchestratorContext.GENERATE:
            return self._handle_itinerary_generation(model)
        elif request_context == OrchestratorContext.UPDATE_DAY:
            return self._handle_day_update(model)
        elif request_context == OrchestratorContext.UPDATE_FULL:
            return self._handle_full_itinerary_update(model)
        else:
            raise RuntimeError("Unknown context : {}", request_context)

    def _handle_itinerary_generation(self, itineraryGenerationRequestModel: ItineraryGenerationRequestModel):
        conversation_id = self.conversation_service.create_conversation()
        if itineraryGenerationRequestModel.user_id is not None:
            self.user_service.add_conversation(conversation_id, itineraryGenerationRequestModel.user_id)

        itinerary = self.llm_service.chat(conversation_id, str(itineraryGenerationRequestModel))
        self.conversation_service.update_conversation(conversation_id, str(itineraryGenerationRequestModel), "user")
        self.conversation_service.update_conversation(conversation_id, message_text=itinerary.model_dump(), role="assistant")
        
        itinerary_id = self.itinerary_service.create_new_itinerary(itinerary)
        self.conversation_service.link_conversation_with_itinerary(conversation_id, itinerary_id)
        if itineraryGenerationRequestModel.user_id is not None:
            self.user_service.add_draft_itinerary(itinerary_id, itineraryGenerationRequestModel.user_id)
        
        return {"conversation_id": conversation_id, "itinerary_id": itinerary_id}


    def _handle_full_itinerary_update(self, itineraryUpdationRequestModel: ItineraryUpdationRequestModel):
        conversation_id = itineraryUpdationRequestModel.conversation_id

        updated_itinerary = self.llm_service.chat(conversation_id, itineraryUpdationRequestModel.user_input)
        self.conversation_service.update_conversation(conversation_id, itineraryUpdationRequestModel.user_input, "user")
        self.conversation_service.update_conversation(conversation_id, updated_itinerary.model_dump(), "assistant")

        self.itinerary_service.update_itinerary(itineraryUpdationRequestModel.itinerary_id, updated_itinerary.model_dump())
        
        return {"conversation_id": conversation_id, "itinerary_id": itineraryUpdationRequestModel.itinerary_id}


    def _handle_day_update(self, itineraryUpdationRequestModel: ItineraryUpdationRequestModel):
        pass


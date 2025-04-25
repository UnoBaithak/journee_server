from pydantic import BaseModel

from conversations import ConversationService
from itinerary import ItineraryService
from models.request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from llm import LLMService
from enum import Enum

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
        # Create an base conversation -> Get an itinerary from llm service -> Save itinerary to DB ->
        # link conversation and itinerary -> return itinerary_id
        conversation_id = self.conversation_service.create_conversation(str(itineraryGenerationRequestModel))
        if itineraryGenerationRequestModel.user_id is not None:
            self.conversation_service.link_conversation_to_user(itineraryGenerationRequestModel.user_id, conversation_id)

        itinerary = self.llm_service.chat(conversation_id, str(itineraryGenerationRequestModel))
        itinerary_id = self.itinerary_service.create_new_itinerary(itinerary)
        self.conversation_service.link_conversation_with_itinerary(conversation_id, itinerary_id)
        self.conversation_service.update_conversation(conversation_id, message_text=itinerary.model_dump(), role="assistant")
        
        return itinerary_id


    def _handle_full_itinerary_update(self, itineraryUpdationRequestModel: ItineraryUpdationRequestModel):
        pass

    def _handle_day_update(self, itineraryUpdationRequestModel: ItineraryUpdationRequestModel):
        pass


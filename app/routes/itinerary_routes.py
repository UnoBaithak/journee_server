from fastapi import APIRouter
from request_models.itinerary_request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from services import Orchestrator
from services.orchestrator_service import OrchestratorContext
from itinerary import ItineraryService
import logging

router = APIRouter(prefix="/api/itinerary")
orchestrator = Orchestrator()
itinerary_service = ItineraryService()
logger = logging.getLogger("uvicorn")

@router.post("/generate")
async def generate_itinerary(itineraryGenerationRequest: ItineraryGenerationRequestModel):
    return await orchestrator.handle(itineraryGenerationRequest, OrchestratorContext.GENERATE)

@router.get("/{itinerary_id}")
async def get_single_itinerary(itinerary_id: str):
    logger.info("Get Itinerary id: " + itinerary_id)
    # TODO: If a logged user tries to get this itinerary, then a enhanced model is sent back
    # that has the particular conversation of that user regarding this itinerary in the model as well
    # this way if a user refreshes then they are still able to converse and updated
    # For now, since we are not checking if user is logged in or not (for code reference to this, can check Zeus)
    # we don't send this enhanced model back
    # Due to this enhanced model being sent back, users don't need to know about the concept of conversation
    # For a user everything is an itinerary and they can edit it normally, its the backend which has the concept
    # of conversation so that LLM has context of user talking about history. 
    # It does not mean that user won't know what a conversation is.. they can obviously look at the history and since
    # enhanced model attaches conversation_id to the itinerary, it will be possible to fetch the history and show to the user
    # What user not being aware means is that they don't explicitly access a conversation, they only access itinerary. 
    return itinerary_service.get_itinerary(itinerary_id)

@router.put("/{itinerary_id}/update")
async def update_full_itinerary(itinerary_id: str, itineraryUpdationRequest: ItineraryUpdationRequestModel):
    logger.info(f"Update full itinerary {itinerary_id}")
    itineraryUpdationRequest.itinerary_id = itinerary_id
    return await orchestrator.handle(itineraryUpdationRequest, OrchestratorContext.UPDATE_FULL)

@router.patch("/{itinerary_id}/day/{day_id}/update")
async def update_day(itinerary_id: str, day_id: str, itineraryUpdateionRequest: ItineraryUpdationRequestModel):
    itineraryUpdateionRequest.itinerary_id = itinerary_id
    itineraryUpdateionRequest.day_id = day_id
    return await orchestrator.handle(itineraryUpdateionRequest, OrchestratorContext.UPDATE_DAY)

@router.get("/")
async def generic_welcome():
    return "On the itinerary route"
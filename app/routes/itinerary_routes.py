from fastapi import APIRouter
from request_models.itinerary_request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from services import Orchestrator
from services.orchestrator_service import OrchestratorContext

router = APIRouter(prefix="/api/itinerary")
orchestrator = Orchestrator()

@router.post("/generate")
async def generate_itinerary(
    itineraryGenerationRequest: ItineraryGenerationRequestModel
):
    return await orchestrator.handle(itineraryGenerationRequest, OrchestratorContext.GENERATE)

@router.post("/update")
async def update_full_itinerary(    
    itineraryUpdationRequest: ItineraryUpdationRequestModel, 
):
    if itineraryUpdationRequest.day_id:
        return await orchestrator.handle(itineraryUpdationRequest, OrchestratorContext.UPDATE_DAY)

    return await orchestrator.handle(itineraryUpdationRequest, OrchestratorContext.UPDATE_FULL)

@router.get("/")
async def generic_welcome():
    return "On the itinerary route"
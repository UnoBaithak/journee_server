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
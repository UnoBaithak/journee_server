from fastapi import APIRouter, Depends
from plan.models.request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from plan.services import Orchestrator
from plan.services.orchestrator_service import OrchestratorContext
from auth.utils import AuthUtils
import logging

router = APIRouter(prefix="/api/plan")
orchestrator = Orchestrator()
logger = logging.getLogger("uvicorn")

@router.post("/")
async def generate_itinerary(itineraryGenerationRequest: ItineraryGenerationRequestModel, 
                             jwt_payload = Depends(AuthUtils.decode_jwt_token)):
    if jwt_payload.get("user_id", None) is not None:
        itineraryGenerationRequest.user_id = jwt_payload["user_id"]
    return await orchestrator.handle(itineraryGenerationRequest, OrchestratorContext.GENERATE)

@router.put("/{itinerary_id}")
async def update_full_itinerary(itinerary_id: str, 
                                itineraryUpdationRequest: ItineraryUpdationRequestModel):
    logger.info(f"Update full itinerary {itinerary_id}")
    itineraryUpdationRequest.itinerary_id = itinerary_id
    await orchestrator.handle(itineraryUpdationRequest, OrchestratorContext.UPDATE_FULL)
    return {"status": "ITINERARY_UPDATED"}

@router.patch("/{itinerary_id}/day/{day_id}")
async def update_day(itinerary_id: str, 
                     day_id: str, 
                     itineraryUpdateionRequest: ItineraryUpdationRequestModel):
    itineraryUpdateionRequest.itinerary_id = itinerary_id
    itineraryUpdateionRequest.day_id = day_id
    await orchestrator.handle(itineraryUpdateionRequest, OrchestratorContext.UPDATE_DAY)
    return {"status": "DAY_UPDATED"}

@router.get("/")
async def generic_welcome():
    return "On the Planmning route" 
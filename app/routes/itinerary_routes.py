from fastapi import APIRouter, Depends
from request_models.itinerary_request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from services import Orchestrator
from services.orchestrator_service import OrchestratorContext
from itinerary import ItineraryService
from auth.utils import AuthUtils
import logging

router = APIRouter(prefix="/api/itinerary")
orchestrator = Orchestrator()
itinerary_service = ItineraryService()
logger = logging.getLogger("uvicorn")

@router.get("/{itinerary_id}")
async def get_single_itinerary(itinerary_id: str, jwt_payload = Depends(AuthUtils.decode_jwt_token)):
    itinerary = itinerary_service.get_itinerary(itinerary_id)
    user_id = jwt_payload.get("user_id", None)
    canEdit = itinerary["metadata"]["creatorId"] == user_id if user_id is not None else False
    return {"itinerary": itinerary, "canEdit": canEdit}

@router.post("/{itinerary_id}/clone")
async def clone_itinerary(itinerary_id: str, jwt_payload = Depends(AuthUtils.decode_jwt_token)):
    user_id = jwt_payload.get("user_id", None)
    return itinerary_service.clone_itinerary(itinerary_id, user_id)
from fastapi import APIRouter, Depends
from itinerary.services import ItineraryService
from auth.utils import AuthUtils
import logging

router = APIRouter(prefix="/api/itinerary")
itinerary_service = ItineraryService()
logger = logging.getLogger("uvicorn")

@router.get("/{itinerary_id}")
async def get_single_itinerary(itinerary_id: str, jwt_payload = Depends(AuthUtils.decode_jwt_token)):
    itinerary = itinerary_service.get_itinerary(itinerary_id)
    user_id = jwt_payload.get("user_id", None)
    if itinerary["metadata"]["creatorId"] is None:
        canEdit = True
    else:
        canEdit = itinerary["metadata"]["creatorId"] == user_id if user_id is not None else False
    
    return {"itinerary": itinerary, "canEdit": canEdit}

@router.post("/{itinerary_id}/clone")
async def clone_itinerary(itinerary_id: str, jwt_payload = Depends(AuthUtils.decode_jwt_token)):
    user_id = jwt_payload.get("user_id", None)
    return itinerary_service.clone_itinerary(itinerary_id, user_id)

@router.post("/{itinerary_id}/save")
async def clone_itinerary(itinerary_id: str, jwt_payload = Depends(AuthUtils.decode_jwt_token)):
    user_id = jwt_payload.get("user_id", None)
    return itinerary_service.save_itinerary(itinerary_id, user_id)
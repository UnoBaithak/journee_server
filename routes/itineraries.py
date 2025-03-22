from fastapi import APIRouter, HTTPException, Depends, Request
from models.request_models import ItineraryGenerationRequestModel, ItineraryUpdationRequestModel
from services.itinerary_generator import ItineraryGenerator
from services.itinerary_updater import ItineraryUpdater

router = APIRouter()

@router.post("/generate")
async def generate_itinerary(
    itineraryGenerationRequest: ItineraryGenerationRequestModel, 
    request: Request
):
    generator = ItineraryGenerator(itineraryGenerationRequest)
    itinerary = await generator.build_and_save()
    return {"status": "SUCCESS", "itinerary": itinerary}

@router.post("/update/{itinerary_id}")
async def update_full_itinerary(
    itinerary_id: str,
    itineraryUpdationRequest: ItineraryUpdationRequestModel, 
):
    updator = ItineraryUpdater(itineraryUpdationRequest.user_input, itinerary_id)
    update_status = await updator.update_full()

    if update_status:
        return {"status": "SUCCESS"}

    return {"status": "FAILURE"}

@router.post("/update/{itinerary_id}/{day_id}")
async def update_single_day(
    itinerary_id: str,
    day_id: str,
    itineraryUpdationRequest: ItineraryUpdationRequestModel, 
):
    updator = ItineraryUpdater(itineraryUpdationRequest.user_input, itinerary_id)
    update_status = await updator.update_single_day(day_id)

    if update_status:
        return {"status": "SUCCESS"}
    
    return {"status": "FAILURE"}

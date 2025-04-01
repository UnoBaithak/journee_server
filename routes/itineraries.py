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
    generator = ItineraryGenerator()
    response = generator.generate_itinerary(itineraryGenerationRequest)
    return response

@router.post("/update")
async def update_full_itinerary(    
    itineraryUpdationRequest: ItineraryUpdationRequestModel, 
):
    itinerary_id = itineraryUpdationRequest.itinerary_id
    day_id = itineraryUpdationRequest.day_id
    updator = ItineraryUpdater(itineraryUpdationRequest.user_input, itinerary_id=itinerary_id)
    update_status = False
    if not day_id:
        update_status = await updator.update_full()
    else:
        update_status = await updator.update_single_day(day_id)

    if update_status:
        return {"status": "SUCCESS"}

    return {"status": "FAILURE"}

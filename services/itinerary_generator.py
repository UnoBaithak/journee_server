from models.request_models import ItineraryGenerationRequestModel
from services.db_service import DBService
from services.llm_service import LLMService

class ItineraryGenerator():
    def __init__(self):
        self.collection = DBService().get_collection("itineraries")
        self.llm_service = LLMService()
    
    def generate_itinerary(self, itineraryGenerationRequest: ItineraryGenerationRequestModel):
        destination = itineraryGenerationRequest.destination
        num_days = itineraryGenerationRequest.num_days
        preferences = itineraryGenerationRequest.preferences

        response = self.llm_service.get_itinerary(destination, num_days, preferences)
        return {"itinerary": response}
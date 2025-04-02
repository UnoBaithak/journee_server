from models.request_models import ItineraryGenerationRequestModel
from services.db_service import DBService
from services.llm_service import LLMService
from models.data_models import Itinerary
from hotspots.metadata_fetcher import MetadataFetcher

class ItineraryGenerator():
    def __init__(self):
        self.collection = DBService().get_collection("itineraries")
        self.llm_service = LLMService()
        self.hotspot_metadata_fetcher = MetadataFetcher()
    
    async def generate_itinerary(self, itineraryGenerationRequest: ItineraryGenerationRequestModel):
        destination = itineraryGenerationRequest.destination
        num_days = itineraryGenerationRequest.num_days
        preferences = itineraryGenerationRequest.preferences

        itinerary: Itinerary = self.llm_service.get_itinerary(destination, num_days, preferences)
        for day in itinerary.details:
            for activity in day.activities:
                for poi in activity.pois:
                    lat, lon = await self.hotspot_metadata_fetcher.get_from_nominatim(f"{poi.name}, {destination}")
                    print(f"{poi.name}: {lat}, {lon}")
                    if lat and lon:
                        poi.lat = lat
                        poi.lon = lon
        
        return {"itinerary": itinerary}
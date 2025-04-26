from app.request_models.itinerary_request_models import ItineraryGenerationRequestModel
from services.db_service import DBService
from llm.llm_service import LLMService
from .models import Itinerary
from hotspots.metadata_fetcher import MetadataFetcher

class ItineraryGenerator:
    def __init__(self):
        self.collection = DBService().get_collection("itineraries")
        self.llm_service = LLMService()
        self.hotspot_metadata_fetcher = MetadataFetcher()
    
    async def generate_itinerary(self, destination, num_days, preferences):

        itinerary: Itinerary = self.llm_service.get_itinerary(destination, num_days, preferences)
        for day in itinerary.details:
            for activity in day.activities:
                for poi in activity.pois:
                    lat, lon = await self.hotspot_metadata_fetcher.get_from_nominatim(f"{poi.name}, {destination}")
                    print(f"{poi.name}: {lat}, {lon}")
                    if lat and lon:
                        poi.lat = lat
                        poi.lon = lon

        result = self.collection.insert_one(itinerary.model_dump())

        return {"itinerary": result.inserted_id}
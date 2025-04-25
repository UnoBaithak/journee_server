import datetime
from typing import Optional

from .itinerary_generator import ItineraryGenerator
from .itinerary_updater import ItineraryUpdater
from services import DBService
from itinerary.models import Itinerary, ItineraryMetadata

class ItineraryService:

    def __init__(self):
        self.itinerary_generator = ItineraryGenerator()
        self.itinerary_updator = ItineraryUpdater()
        self.collection = DBService().get_collection("itinerary")

    def create_new_itinerary(self, itinerary: Itinerary):
        result = self.collection.insert_one(itinerary.model_dump())
        return str(result.inserted_id)

    def update_full_itinerary(self, itinerary_id: str, new_itinerary: Itinerary):
        self.collection.update_one()

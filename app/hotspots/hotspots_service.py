from hotspots.geolocation_fetcher import GeolocationFetcher
from itinerary.models import Itinerary

import logging

logger = logging.getLogger("uvicorn")

class HotspotService:
    """Service to manage fetching and ranking hotspots"""

    def __init__(self):
        self.geolocation_fetcher = GeolocationFetcher()

    async def populate_hotspot_metadata(self, itinerary: Itinerary):
        for dayDetails in itinerary.details:
            for activity in dayDetails.activities:
                for poi in activity.pois:
                    logger.info("Get latitude and longitude for " + poi.name + "," + itinerary.metadata.destination)
                    lat, long = await self.get_lat_lon(f"{poi.name},{itinerary.metadata.destination}")
                    if lat and long:
                        logger.info("Updating latitude and longitude for " + poi.name)
                        poi.lat = lat
                        poi.lon = long

    async def get_lat_lon(self, location: str):
        return await self.geolocation_fetcher.get_from_nominatim(location)

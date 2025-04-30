import logging
import httpx
logger = logging.getLogger("uvicorn")

class GeolocationFetcher:
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

    async def get_from_nominatim(self, destination: str):
        """Fetch Lat/Lon from Nominatim API"""
        logger.info(f"Fetching Lat/Lon for '{destination}' using Nominatim")

        params = {"q": destination, "format": "json", "limit": 1}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.NOMINATIM_URL, params=params)

        if response.status_code != 200 or not response.json():
            logger.error(f"Failed to fetch Lat/Lon for '{destination}'")
            return None, None

        data = response.json()[0]
        lat, lon = float(data["lat"]), float(data["lon"])
        return lat, lon
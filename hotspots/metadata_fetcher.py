import logging
import httpx
logger = logging.getLogger("__name__")

class MetadataFetcher:
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

    async def get_lat_lon(self, destination: str):
        lat, lon = await self.get_from_db(destination)
        if lat and lon:
            return lat, lon
        
        return await self.get_from_nominatim(destination)

    async def get_from_db(self, destination: str):
        """Fetch Lat/Lon from DB (if available)"""
        # TODO: Add DB query logic here (MongoDB or SQL)
        print(f"Checking DB for destination: {destination}")
        return None, None

    async def get_from_nominatim(self, destination: str):
        """Fetch Lat/Lon from Nominatim API"""
        print(f"Fetching Lat/Lon for '{destination}' using Nominatim")

        params = {"q": destination, "format": "json", "limit": 1}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.NOMINATIM_URL, params=params)

        if response.status_code != 200 or not response.json():
            print(f"Failed to fetch Lat/Lon for '{destination}'")
            return None, None

        data = response.json()[0]
        lat, lon = float(data["lat"]), float(data["lon"])
        return lat, lon
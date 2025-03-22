import httpx
from models.data_models import PointOfInterest
import logging
from typing import List
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger("OverpassFetcher")

class OverpassDataFetcher():
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    
    async def fetch_hotspots(self, lat, lon, radius=3000, category="tourism"):
        query=f"""
        [out:json];
        (
            node(around:{radius},{lat},{lon})["{category}"];
            way(around:{radius},{lat},{lon})["{category}"];
            relation(around:{radius},{lat},{lon})["{category}"];
        );
        out center;
        """
        print(f"Fetching hotspots for category '{category}' near [{lat}, {lon}] in a radius of {radius}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.OVERPASS_URL, data={"data": query})
        
        if response.status_code != 200:
            print(f"Error in fetching hotspots: {response.text}")
            return []

        data = response.json()
        return self.parse_hotspots(data)
    
    def parse_hotspots(self, data) -> List[PointOfInterest]:
        elements = data.get("elements", [])
        pois = []

        for element in elements:
            lat, lon = element.get("lat"), element.get("lon")
            tags = element.get("tags", {})
            if "name" in tags:
                pois.append(
                    PointOfInterest(
                        name=tags["name"],
                        lat = lat,
                        lon = lon,
                        category=tags.get("tourism", "unknown"),
                        description=tags.get("description", ""),
                        website=tags.get("website", "")
                    )
                )
        
        print(f"Found {len(pois)} points of interest")
        return pois

from hotspots.metadata_fetcher import MetadataFetcher

import logging

logger = logging.getLogger(__name__)

class HotspotService:
    """Service to manage fetching and ranking hotspots"""

    def __init__(self):
        self.metadata_fetcher = MetadataFetcher()

    async def get_top_hotspots(self, destination: str, num_results=5, radius=10000):
        """Get top hotspots for a given destination"""
        print("Fetching lat lon")
        lat, lon = await self.metadata_fetcher.get_lat_lon(destination)

        if not lat or not lon:
            print("Could not fetch")
            logger.warning(f"Could not fetch Lat/Lon for destination: {destination}")
            return []

        all_hotspots = await self.overpass_fetcher.fetch_hotspots(lat, lon, radius)

        # ✅ Basic Ranking Logic (Can be Enhanced Later)
        ranked_hotspots = sorted(all_hotspots, key=lambda x: len(x.name), reverse=True)

        # ✅ Return Top N Hotspots
        top_hotspots = ranked_hotspots[:num_results]
        print(f"Returning top {len(top_hotspots)} hotspots.")
        return top_hotspots
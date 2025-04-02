import os
from llm.llmclient_factory import LLMClientFactory

class LLMService:
    def __init__(self):
        self.client = LLMClientFactory.get_llm_client(os.getenv("MODEL_NAME"),
                                                    os.getenv("API_KEY"))
        self.base_prompt = """You are a world-class travel planner, and you need to plan a medium-budget trip with the following details:
        Destination: {destination}
        Number of Days: {num_days}
        Preferences: {preferences}
	
    Guidelines for Planning:
		1.	No Hallucination – Only include real places and activities. If there are not enough points of interest to fill all days, do not invent locations or attractions.
	    2.	Precision & Detail – Be specific about each location, providing concrete details about attractions, historical significance, best visiting hours, and any notable features. Avoid generic or vague descriptions.
	    3.	Balance Between Activities:
	        •	For a packed itinerary: Include at least two well-defined activities per day.
	        •	For a relaxed itinerary: Include at most three activities per day.
	    4.	Handling Multi-City Travel: If the itinerary involves visiting multiple cities, allocate at least one day for travel and self-leisure (walking around, exploring casually, etc.).
	    5.	Handling Market Visits & Self-Exploration:
	        •	If an activity involves visiting a physical landmark, attraction, or place of interest, mark it as a point of interest.
	        •	If an activity involves general self-exploration, walking, visiting local markets, or travel hubs, do not classify it as a point of interest.
"""

    def get_itinerary(self, destination, num_days, preferences):
        user_prompt = self.base_prompt.format(destination=destination,num_days=num_days,preferences=preferences)
        response = self.client.generate_text(user_prompt)
        return response

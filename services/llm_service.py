import os
from llm.llmclient_factory import LLMClientFactory

class LLMService:
    def __init__(self):
        self.client = LLMClientFactory.get_llm_client(os.getenv("MODEL_NAME"),
                                                    os.getenv("API_KEY"))
        self.base_prompt = """You are a world class travel planner and you need to plan a medium budget trip with the following information. 
Destination: {destination}
Number of Days: {num_days}
Preferences: {preferences}

Plan for each day, do not be vague, be precise. Describe whatever you can about the spots / points of interests. If its a multi-city travel, assume at least a day for travel and self leisure to explore on foot.
If a packed itinerary is planned, try to have at least two activities in a day, whereas for a relaxed itinerary at most three activities per day. The number of days is an upper limit, but if all of them are not being filled, a few days less is acceptable as per the mood.
Also in the structured output, do not fill anything for the metadata sections
"""

    def get_itinerary(self, destination, num_days, preferences):
        user_prompt = self.base_prompt.format(destination=destination,num_days=num_days,preferences=preferences)
        response = self.client.generate_text(user_prompt)
        return response

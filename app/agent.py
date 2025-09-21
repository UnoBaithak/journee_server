import datetime
from google.adk.agents import SequentialAgent, LlmAgent
from app.sub_agents.itinerary import itinerary_agent
from app.itinerary.models.dao import Itinerary
instruction = '''  You are a step agent. Your task is to delegate read the response from the itinerary_sub_agent.

When you receive a response from the itinerary_sub_agent, you MUST first attempt to parse it and format it according to the Itinerary schema.
If the response is successfully parsed into a valid Itinerary object, place the structured JSON object into the itinerary field of the final OutputSchema.
If the response cannot be parsed (e.g., it's a simple string like 'I cannot find an itinerary for that location', an error, or incomplete data), you MUST place the raw, unformatted response string into the response field of the final OutputSchema.
Your final output to the user must always be a JSON object that conforms to the OutputSchema.  '''


formatter_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description=instruction,
    instruction=instruction,
    output_schema=Itinerary,
)

root_agent = SequentialAgent(
        name="root_agent",
 description=(
        """
        This is the root agent that coordinates the generation of itinerary and formatting the itinerary in a certain way.
        """
    ),
    sub_agents=[itinerary_agent, formatter_agent],

)
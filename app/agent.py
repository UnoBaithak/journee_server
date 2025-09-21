import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from app.tools import get_flights, get_hotels, get_tourist_attractions


root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description=(
        "You are a helpful agent who helps with travel planning. " + 
        "When a user asks for an itinerary, you must use the 'itinerary_agent' tool. " + 
        "The output from 'itinerary_agent' is the final answer and should be presented directly to the user without any summarization, rephrasing, or additional comments." + 
        "If a user asks for flight details you must use the 'flight_agent' tool" + 
        "The output of 'flight_agent'  is the final answer and should be presented directly to the user without any summarization, rephrasing, or additional comments." 
    ),
    instruction=(
    "You are a highly capable travel planning agent. " +
    "When a user requests an points of interest for a given place, you must use the 'get_tourist_attractions' tool. " +
    "If a user asks for flight details, you must use the 'get_flights' tool. " +
    "If a user asks for hotel details, you must use the 'get_hotels' tool. " +
    "When a user requests an itinerary or comprehensive trip planning, you must use all relevant tools " +
    "(get_tourist_attractions, get_flights, get_hotels) as needed to provide a detailed itinerary that includes: " +
    "complete day-by-day schedule containing good points of interest (from 'get_tourist_attractions'), relevant flight options (from 'get_flights'), " +
    "suitable hotels or accommodation options (from 'get_hotels'), and suggestions for places to visit, activities, " +
    "and experiences at each destination. " +
    "Your mission is to deliver accurate, actionable, and detailed travel plans using specialized tools, " +
    "ensuring the user receives all necessary details for a seamless trip. All this in an easily understandable human readble format."
    ),
    tools=[get_tourist_attractions, get_flights, get_hotels],
)
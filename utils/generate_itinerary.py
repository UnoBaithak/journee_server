import google.generativeai as genai
from utils.parse_itinerary import parse_itinerary
import os

def generate_itinerary(destination, duration, budget, preferences, start_date, end_date):
    """
    Generates a day-wise travel itinerary based on user-specified parameters using Gemini AI.

    Args:
        destination (str): The main travel destination.
        duration (int): Number of days for the trip.
        budget (str): Budget category ('low', 'medium', 'high').
        preferences (list): List of travel preferences (e.g., ['cultural attractions', 'adventure']).
        start_date (str): Start date of the trip in "YYYY-MM-DD" format.
        end_date (str): End date of the trip in "YYYY-MM-DD" format.

    Returns:
        dict: A structured itinerary broken down by days with additional options (if any).
    """
    prompt = f"""
    You are a travel planning assistant. Generate a {duration}-day travel itinerary for {destination}.
    The trip is scheduled from {start_date} to {end_date}.
    The itinerary should include day-wise activities, attractions, and accommodations for each day.
    Consider the following:
    - Budget: {budget}
    - Preferences: {', '.join(preferences)}

    Provide the response in plain text format, clearly labeled with "Day X:", "Activities:", and "Notes:" sections.
    Include an "Additional Options:" section for budget and stay options.
    """

    try:
        genai.configure(api_key=os.getenv("GENAI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return parse_itinerary(response.text)

    except Exception as e:
        return {"error": f"Unable to fetch itinerary at this time. {str(e)}"}

import re

def parse_itinerary(response_text):
    """
    Parses the itinerary from Gemini's string output into a structured object.

    Args:
        response_text (str): Raw string output from Gemini AI.

    Returns:
        dict: Parsed itinerary data structured into a dictionary.
    """
    itinerary = {"days": {}, "options": {}}

    # Regular expression to match "Day X:" blocks
    day_pattern = re.compile(r"(Day \d+):\s*(.*?)\s*(?=Day \d+:|$)", re.DOTALL)
    day_matches = day_pattern.findall(response_text)

    # Process each day block
    for day, details in day_matches:
        activities_pattern = re.compile(r"Activities:\s*(.*?)(?:Notes:|$)", re.DOTALL)
        notes_pattern = re.compile(r"Notes:\s*(.*)", re.DOTALL)

        activities_match = activities_pattern.search(details)
        notes_match = notes_pattern.search(details)

        activities = [
            act.strip("- ") for act in activities_match.group(1).strip().split("\n") if act.strip()
        ] if activities_match else []
        notes = notes_match.group(1).strip() if notes_match else "No additional notes"

        itinerary["days"][day] = {
            "activities": activities,
            "notes": notes,
        }

    # Extract options (if available)
    options_pattern = re.compile(r"Additional Options:\s*(.*?)$", re.DOTALL)
    options_match = options_pattern.search(response_text)

    if options_match:
        options_text = options_match.group(1)
        for line in options_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                itinerary["options"][key.strip().lower()] = value.strip()

    return itinerary

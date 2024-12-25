from flask import Flask, request, jsonify
from utils.generate_itinerary import generate_itinerary

app = Flask(__name__)


@app.route("/generate-itinerary", methods=["POST"])
def generate_itinerary_endpoint():
    data = request.get_json()

    # Validate input data
    required_fields = ["destination", "duration", "budget", "preferences", "start_date", "end_date"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        destination = data["destination"]
        duration = int(data["duration"])
        budget = data["budget"].lower()
        preferences = data["preferences"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        # Generate the itinerary
        itinerary = generate_itinerary(destination, duration, budget, preferences, start_date, end_date)

        if "error" in itinerary:
            return jsonify(itinerary), 500

        return jsonify(itinerary), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run on all available network interfaces, port 5000

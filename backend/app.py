from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import math
import random
import polyline

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImVlYmM0ODAxNzBjOTQ1Y2E5ZGU1M2U2NzY3YzkwYTEzIiwiaCI6Im11cm11cjY0In0="



# Define events
EVENTS = {
    "concert": {"lat": 28.539, "lon": -81.383, "radius_km": 1.0, "slow_factor": 1.5},
    "football": {"lat": 28.592, "lon": -81.204, "radius_km": 1.2, "slow_factor": 1.7}
}

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance in km
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

TOMTOM_KEY = "e0GCpBun6qwRTDLFMmmpt2rnY5CG5apt"

@app.route("/api/traffic_route")
def traffic_route():

    start_lat = request.args.get("start_lat")
    start_lon = request.args.get("start_lon")
    end_lat = request.args.get("end_lat")
    end_lon = request.args.get("end_lon")

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_lat},{start_lon}:{end_lat},{end_lon}/json?key={TOMTOM_KEY}&traffic=true&maxAlternatives=2"

    r = requests.get(url)
    data = r.json()

    if "routes" not in data:
        return jsonify({"error": data}), 500

    routes_output = []

    for route in data["routes"]:

        coords = [
            [p["latitude"], p["longitude"]]
            for p in route["legs"][0]["points"]
        ]

        duration = route["summary"]["travelTimeInSeconds"]

        routes_output.append({
            "coords": coords,
            "duration": duration
        })

    return jsonify({"routes": routes_output}) 


if __name__ == "__main__":
    app.run(debug=True)

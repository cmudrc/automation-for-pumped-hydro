import os
import requests
import pandas as pd

def fetch_grocery_stores(api_key: str, reservoir_lat: float, reservoir_lon: float, radius: float = 80000.0): #50mile
    """
    Fetch grocery store locations near a given reservoir.
    :param api_key: Google Maps API key.
    :param reservoir_lat: Latitude of the reservoir.
    :param reservoir_lon: Longitude of the reservoir.
    :param radius: Search radius in meters (default: 50 miles).
    :return: DataFrame with grocery store names and their lat/lon.
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{reservoir_lat},{reservoir_lon}",
        "radius": radius,
        "type": "grocery_or_supermarket",
        "key": os.getenv("GOOGLE_MAPS_API_KEY"),
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        raise ValueError("No grocery stores found or invalid API response")

    stores = [
        {
            "latitude": store["geometry"]["location"]["lat"],
            "longitude": store["geometry"]["location"]["lng"],
        }
        for store in data["results"]
    ]

    return pd.DataFrame(stores)

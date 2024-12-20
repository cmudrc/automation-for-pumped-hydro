import os

import pandas
import requests


def fetch_grocery_stores(
    reservoir_lat: float, reservoir_lon: float, radius: float = 80000.0
):
    """
    Fetch grocery store locations near a given reservoir.
    :param reservoir_lat: Latitude of the reservoir.
    :type reservoir_lat: float
    :param reservoir_lon: Longitude of the reservoir.
    :type reservoir_lon: float
    :param radius: Search radius in meters (default: 50 miles).
    :type radius: float
    :return: DataFrame with grocery store names and their lat/lon.
    :rtype: pandas.DataFrame
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

    return pandas.DataFrame(stores)

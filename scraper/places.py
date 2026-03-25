import requests
from config import GOOGLE_PLACES_KEY, COMPETITOR_LIMIT, SEARCH_RADIUS_METERS


def find_clinic(name: str, location: str) -> dict | None:
    search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": f"{name} dental {location}",
        "inputtype": "textquery",
        "fields": "place_id,name,formatted_address,geometry",
        "key": GOOGLE_PLACES_KEY,
    }
    resp = requests.get(search_url, params=params).json()
    candidates = resp.get("candidates", [])
    return candidates[0] if candidates else None


def find_competitors(lat: float, lng: float, exclude_place_id: str) -> list[dict]:
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": SEARCH_RADIUS_METERS,
        "keyword": "dental clinic",
        "key": GOOGLE_PLACES_KEY,
    }
    resp = requests.get(nearby_url, params=params).json()
    results = resp.get("results", [])
    competitors = [r for r in results if r.get("place_id") != exclude_place_id]
    return competitors[:COMPETITOR_LIMIT]


def get_place_details(place_id: str) -> dict:
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,price_level,opening_hours,photos,reviews,formatted_address,url",
        "key": GOOGLE_PLACES_KEY,
    }
    resp = requests.get(details_url, params=params).json()
    return resp.get("result", {})

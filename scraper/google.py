from config import MAX_REVIEWS_PER_SOURCE


def extract_google_reviews(place_details: dict) -> list[dict]:
    raw = place_details.get("reviews", [])
    reviews = []

    for r in raw[:MAX_REVIEWS_PER_SOURCE]:
        text = r.get("text", "").strip()
        if len(text) > 30:
            reviews.append({
                "source": "google",
                "text": text,
                "rating": r.get("rating"),
                "time": r.get("relative_time_description"),
            })

    return reviews


def extract_clinic_metrics(place_details: dict) -> dict:
    hours = place_details.get("opening_hours", {})
    return {
        "name": place_details.get("name"),
        "address": place_details.get("formatted_address"),
        "google_rating": place_details.get("rating"),
        "review_count": place_details.get("user_ratings_total"),
        "price_tier": place_details.get("price_level"),
        "open_now": hours.get("open_now"),
        "weekday_hours": hours.get("weekday_text", []),
        "photo_count": len(place_details.get("photos", [])),
        "maps_url": place_details.get("url"),
    }

import sys
from scraper.places import find_clinic, find_competitors, get_place_details
from scraper.google import extract_google_reviews, extract_clinic_metrics
from scraper.yelp import get_yelp_data
from analysis.claude import analyze_competitive_landscape
from report.builder import generate_report


def run(clinic_name: str, location: str):
    print(f"Looking up: {clinic_name} in {location}")

    clinic = find_clinic(clinic_name, location)
    if not clinic:
        print("Could not find that clinic on Google Places. Try a more specific name or location.")
        sys.exit(1)

    place_id = clinic["place_id"]
    lat = clinic["geometry"]["location"]["lat"]
    lng = clinic["geometry"]["location"]["lng"]

    print("Fetching clinic details and reviews...")
    target_details = get_place_details(place_id)
    target_metrics = extract_clinic_metrics(target_details)
    google_reviews = extract_google_reviews(target_details)
    yelp_data = get_yelp_data(clinic_name, location)
    all_reviews = google_reviews + yelp_data["reviews"]

    target = {"metrics": target_metrics, "reviews": all_reviews}

    print("Finding competitors")
    competitor_places = find_competitors(lat, lng, place_id)
    competitors = []
    for cp in competitor_places:
        details = get_place_details(cp["place_id"])
        metrics = extract_clinic_metrics(details)
        reviews = extract_google_reviews(details)
        competitors.append({"metrics": metrics, "reviews": reviews})

    print(f"Found {len(competitors)} competitors and running analysis now")
    analysis = analyze_competitive_landscape(target, competitors)

    print("Building report")
    output_path = generate_report(target, competitors, analysis)

    print(f"\nDone the report has been saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py \"Clinic Name\" \"City, State\"")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])

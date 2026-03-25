import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_PLACES_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

MAX_REVIEWS_PER_SOURCE = 20
COMPETITOR_LIMIT = 5
SEARCH_RADIUS_METERS = 8000

if not ANTHROPIC_KEY or not GOOGLE_PLACES_KEY:
    raise EnvironmentError("Missing required API keys. Check your .env file against .env.example.")

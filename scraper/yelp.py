import requests
from bs4 import BeautifulSoup
from config import MAX_REVIEWS_PER_SOURCE

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def search_yelp(clinic_name: str, location: str) -> str | None:
    query = f"{clinic_name} dental {location}".replace(" ", "+")
    search_url = f"https://www.yelp.com/search?find_desc={query}&find_loc={location}"
    resp = requests.get(search_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    first_result = soup.select_one('a[href*="/biz/"]')
    if not first_result:
        return None
    href = first_result.get("href", "")
    if href.startswith("/biz/"):
        return "https://www.yelp.com" + href.split("?")[0]
    return None


def scrape_reviews(yelp_url: str) -> list[dict]:
    resp = requests.get(yelp_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    reviews = []
    review_blocks = soup.select('p[lang="en"]')

    for block in review_blocks[:MAX_REVIEWS_PER_SOURCE]:
        text = block.get_text(strip=True)
        if len(text) > 30:
            reviews.append({"source": "yelp", "text": text})

    return reviews


def get_yelp_data(clinic_name: str, location: str) -> dict:
    url = search_yelp(clinic_name, location)
    if not url:
        return {"url": None, "reviews": []}

    reviews = scrape_reviews(url)
    return {"url": url, "reviews": reviews}

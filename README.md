# dental-intel

A competitive and public intelligence tool for all dental clinics. Give it a clinic name and location so it can pull public review data from Google and Yelp, finds nearby competitors, and uses Claude to generate a structured analysis of where the clinic stands, what it's doing well, and where it's losing ground.

Built this after working on data pipelines for dental clients and noticing that most practices have no real visibility into how they compare to competitors a mile away.

## What it does

- Looks up the target clinic via Google Places API
- Pulls reviews and metrics (rating, review count, photos, hours, price tier)
- Scrapes Yelp reviews via BeautifulSoup
- Finds up to 5 nearby competitor clinics and pulls their data
- Sends everything to Claude for competitive analysis
- Outputs a clean HTML report with sentiment breakdown, strengths/weaknesses, competitor threats, and quick wins

## Setup

```bash
git clone https://github.com/yourusername/dental-intel.git
cd dental-intel
pip install -r requirements.txt
cp .env.example .env
```

Requirements:
- [Anthropic API key](https://console.anthropic.com/)
- [Google Places API key](https://developers.google.com/maps/documentation/places/web-service/get-api-key)

## Usage

```bash
python main.py "Smile Dental" "Austin, TX"
```

Report is saved to `output/` as an HTML file. Open it in any browser.

## Stack

Python 3.11 · BeautifulSoup · Google Places API · Anthropic API · vanilla HTML/CSS output

## Notes

Yelp scraping works on public pages but can be inconsistent depending on how Yelp renders results in your region. Google Places review data is limited to the most recent 5 reviews per place by the API. The analysis quality scales with how many reviews are available.

This is a portfolio resume project. Not affiliated with any dental practice or platform.

## Sample Output

<img width="1065" height="4182" alt="_C__Users_micha_Downloads_dental-intel_dental-intel_output_bright_now!_dental_ _orthodontics_-_phoenix_(camelback_rd)_intel html (2)" src="https://github.com/user-attachments/assets/8671edcb-2ef9-4f16-b183-49fd2452c42a" />



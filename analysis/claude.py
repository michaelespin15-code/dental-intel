import json
import anthropic
from config import ANTHROPIC_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)


def build_clinic_summary(metrics: dict, reviews: list[dict]) -> str:
    review_block = "\n".join(f"- [{r['source'].upper()}] {r['text']}" for r in reviews)
    hours = "\n".join(metrics.get("weekday_hours", [])) or "Not available"

    return f"""
Clinic: {metrics.get('name')}
Address: {metrics.get('address')}
Google Rating: {metrics.get('google_rating')} ({metrics.get('review_count')} reviews)
Price Tier: {metrics.get('price_tier') or 'Unknown'}
Photos on Google: {metrics.get('photo_count')}
Hours:
{hours}

Reviews:
{review_block or 'No reviews available.'}
""".strip()


def analyze_competitive_landscape(target: dict, competitors: list[dict]) -> dict:
    target_summary = build_clinic_summary(target["metrics"], target["reviews"])
    competitor_summaries = "\n\n---\n\n".join(
        f"Competitor {i+1}:\n{build_clinic_summary(c['metrics'], c['reviews'])}"
        for i, c in enumerate(competitors)
    )

    prompt = f"""You are a dental practice business analyst. You have data on a target dental clinic and its local competitors. Analyze this data and return a JSON object with the following structure:

{{
  "overall_position": "1-2 sentence summary of where the target clinic stands vs competitors",
  "strengths": ["list of 3-5 specific strengths based on the data"],
  "weaknesses": ["list of 3-5 specific weaknesses or gaps"],
  "competitor_threats": ["list of 2-3 specific competitors worth watching and why"],
  "quick_wins": ["list of 3-5 actionable improvements the clinic could make based on what competitors do better"],
  "sentiment_breakdown": {{
    "positive_themes": ["top 3-4 recurring positive themes from reviews"],
    "negative_themes": ["top 3-4 recurring negative themes from reviews"]
  }}
}}

Return only valid JSON. No explanation, no markdown formatting.

TARGET CLINIC:
{target_summary}

COMPETITORS:
{competitor_summaries}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text.strip().removeprefix("```json").removesuffix("```").strip()
    if not raw:
        raise ValueError("Claude returned an empty response. Check your API key and model name.")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("Claude raw response:", raw[:500])
        raise

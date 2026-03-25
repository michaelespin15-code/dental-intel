import os
from datetime import datetime


def render_tag_list(items: list[str], color: str) -> str:
    return "".join(f'<span class="tag {color}">{item}</span>' for item in items)


def render_metric_row(label: str, value) -> str:
    display = value if value is not None else "—"
    return f'<tr><td class="label">{label}</td><td>{display}</td></tr>'


def build_competitor_cards(competitors: list[dict]) -> str:
    cards = []
    for c in competitors:
        m = c["metrics"]
        cards.append(f"""
        <div class="competitor-card">
            <h4>{m.get('name', 'Unknown')}</h4>
            <p class="address">{m.get('address', '')}</p>
            <div class="mini-stats">
                <span>⭐ {m.get('google_rating', '—')}</span>
                <span>📝 {m.get('review_count', '—')} reviews</span>
                <span>📷 {m.get('photo_count', 0)} photos</span>
            </div>
        </div>
        """)
    return "\n".join(cards)


def generate_report(target: dict, competitors: list[dict], analysis: dict, output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)

    m = target["metrics"]
    clinic_name = m.get("name", "Unknown Clinic")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = clinic_name.lower().replace(" ", "_") + "_intel.html"
    filepath = os.path.join(output_dir, filename)

    strengths_html = render_tag_list(analysis.get("strengths", []), "green")
    weaknesses_html = render_tag_list(analysis.get("weaknesses", []), "red")
    threats_html = render_tag_list(analysis.get("competitor_threats", []), "orange")
    wins_html = render_tag_list(analysis.get("quick_wins", []), "blue")
    pos_themes_html = render_tag_list(analysis.get("sentiment_breakdown", {}).get("positive_themes", []), "green")
    neg_themes_html = render_tag_list(analysis.get("sentiment_breakdown", {}).get("negative_themes", []), "red")
    competitor_cards_html = build_competitor_cards(competitors)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{clinic_name} — Competitive Intelligence Report</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f4f6f9; color: #1a1a2e; }}
        header {{ background: #1a1a2e; color: white; padding: 32px 48px; }}
        header h1 {{ font-size: 1.6rem; font-weight: 600; }}
        header p {{ color: #a0aec0; font-size: 0.85rem; margin-top: 4px; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 40px 24px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
        .card {{ background: white; border-radius: 10px; padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); }}
        .card h3 {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #718096; margin-bottom: 16px; }}
        .card.full {{ grid-column: 1 / -1; }}
        .position-text {{ font-size: 1rem; line-height: 1.7; color: #2d3748; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td {{ padding: 8px 4px; font-size: 0.9rem; border-bottom: 1px solid #f0f0f0; }}
        td.label {{ color: #718096; width: 40%; }}
        .tag {{ display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; margin: 4px; line-height: 1.4; }}
        .tag.green {{ background: #f0fff4; color: #276749; }}
        .tag.red {{ background: #fff5f5; color: #9b2c2c; }}
        .tag.orange {{ background: #fffaf0; color: #c05621; }}
        .tag.blue {{ background: #ebf8ff; color: #2b6cb0; }}
        .competitor-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; margin-top: 8px; }}
        .competitor-card {{ background: #f9fafb; border-radius: 8px; padding: 16px; border: 1px solid #e2e8f0; }}
        .competitor-card h4 {{ font-size: 0.9rem; font-weight: 600; margin-bottom: 4px; }}
        .competitor-card .address {{ font-size: 0.75rem; color: #718096; margin-bottom: 10px; }}
        .mini-stats {{ display: flex; gap: 10px; flex-wrap: wrap; font-size: 0.78rem; color: #4a5568; }}
        footer {{ text-align: center; padding: 32px; font-size: 0.78rem; color: #a0aec0; }}
    </style>
</head>
<body>
    <header>
        <h1>{clinic_name} — Competitive Intelligence Report</h1>
        <p>Generated {timestamp} · Powered by Google Places + Yelp + Claude</p>
    </header>
    <div class="container">
        <div class="grid">
            <div class="card full">
                <h3>Market Position</h3>
                <p class="position-text">{analysis.get('overall_position', '—')}</p>
            </div>
            <div class="card">
                <h3>Clinic Metrics</h3>
                <table>
                    {render_metric_row('Google Rating', m.get('google_rating'))}
                    {render_metric_row('Total Reviews', m.get('review_count'))}
                    {render_metric_row('Photos on Google', m.get('photo_count'))}
                    {render_metric_row('Price Tier', m.get('price_tier'))}
                    {render_metric_row('Open Now', m.get('open_now'))}
                </table>
            </div>
            <div class="card">
                <h3>Review Sentiment</h3>
                <p style="font-size:0.8rem;color:#718096;margin-bottom:8px;">Positive themes</p>
                {pos_themes_html}
                <p style="font-size:0.8rem;color:#718096;margin:12px 0 8px;">Negative themes</p>
                {neg_themes_html}
            </div>
            <div class="card">
                <h3>Strengths</h3>
                {strengths_html}
            </div>
            <div class="card">
                <h3>Weaknesses</h3>
                {weaknesses_html}
            </div>
            <div class="card">
                <h3>Competitor Threats</h3>
                {threats_html}
            </div>
            <div class="card">
                <h3>Quick Wins</h3>
                {wins_html}
            </div>
            <div class="card full">
                <h3>Nearby Competitors ({len(competitors)} found)</h3>
                <div class="competitor-grid">
                    {competitor_cards_html}
                </div>
            </div>
        </div>
    </div>
    <footer>dental-intel · github.com/yourusername/dental-intel</footer>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath

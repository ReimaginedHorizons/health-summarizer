from flask import Flask, render_template, request
import feedparser
import requests
import os

app = Flask(__name__)

# Load your API key securely from environment variables
API_KEY = os.environ.get("DEEPSEEK_API_KEY")  # ✅ Set this in Render.com

# Example RSS feeds for health & longevity articles
RSS_FEEDS = [
    "https://www.medicalnewstoday.com/rss",
    "https://www.sciencedaily.com/rss/health_medicine.xml",
    "https://www.nih.gov/news-events/news-releases/rss.xml"
]

def fetch_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # Limit to 5 articles per feed
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'summary': summarize(entry.summary)
            })
    return articles

def summarize(text):
    # This function would use your AI API (like DeepSeek) to summarize
    if not API_KEY:
        return "No API key provided."

    api_url = "https://api.deepseek.com/summarize"  # Replace with actual endpoint
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "text": text,
        "length": "short"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        summary = response.json().get("summary", "No summary returned.")
        return summary
    except Exception as e:
        return f"Summary error: {e}"

@app.route("/")
def index():
    articles = fetch_articles()
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)

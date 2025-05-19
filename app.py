from flask import Flask, render_template
import feedparser
import requests

app = Flask(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-c364a35a252d4281a9b99e7659b82693"  # Put your key here

# Use a health-focused RSS feed (or multiple)
RSS_FEEDS = [
    "https://www.medicalnewstoday.com/rss", 
    "https://www.healthline.com/rss",
    "https://www.nih.gov/news-events/news-releases/rss.xml"
]

def get_articles():
    entries = []
    for feed in RSS_FEEDS:
        parsed = feedparser.parse(feed)
        entries.extend(parsed.entries[:3])  # Limit per feed
    return entries[:5]  # Top 5 overall

def summarize_article(text):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": f"Summarize this for a beginner in 3 sentences:\n\n{text}"}
        ]
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=20)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return "Summary failed. Try again later."

@app.route("/")
def index():
    articles = get_articles()
    summarized = []
    for art in articles:
        summary = summarize_article(art.get("summary", art.get("description", "")))
        summarized.append({
            "title": art.title,
            "link": art.link,
            "summary": summary
        })
    return render_template("index.html", articles=summarized)

if __name__ == "__main__":
    app.run(debug=True)

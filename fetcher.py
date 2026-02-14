import feedparser
import requests
from datetime import datetime
from time import mktime
from database import insert_article

RSS_FEEDS = [
    ("https://rss.arxiv.org/rss/cs.AI", "ArXiv CS.AI", "research"),
    ("https://www.technologyreview.com/feed/", "MIT Tech Review", "news"),
    ("https://openai.com/blog/rss.xml", "OpenAI Blog", "blog"),
    ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge AI", "news"),
]

REDDIT_URL = "https://www.reddit.com/r/artificial/hot.json?limit=30"
HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

HEADERS = {"User-Agent": "AI-News-Aggregator/1.0"}

AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "neural network", "gpt", "llm", "transformer", "openai", "anthropic",
    "chatgpt", "claude", "gemini", "diffusion", "generative",
]


def fetch_rss(url, source_name, category="general"):
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:30]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", "")
            if summary:
                # Strip HTML tags roughly
                import re
                summary = re.sub(r"<[^>]+>", "", summary)[:300]

            published_at = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_at = datetime.fromtimestamp(mktime(entry.published_parsed)).isoformat()
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published_at = datetime.fromtimestamp(mktime(entry.updated_parsed)).isoformat()

            if title and link:
                insert_article(title, link, source_name, category, summary, published_at)
    except Exception as e:
        print(f"[RSS Error] {source_name}: {e}")


def fetch_hackernews():
    try:
        resp = requests.get(HN_TOP_URL, headers=HEADERS, timeout=10)
        story_ids = resp.json()[:100]

        for sid in story_ids:
            try:
                item = requests.get(HN_ITEM_URL.format(sid), headers=HEADERS, timeout=5).json()
                if not item or item.get("type") != "story":
                    continue

                title = item.get("title", "")
                url = item.get("url", f"https://news.ycombinator.com/item?id={sid}")
                title_lower = title.lower()

                if not any(kw in title_lower for kw in AI_KEYWORDS):
                    continue

                published_at = None
                if item.get("time"):
                    published_at = datetime.fromtimestamp(item["time"]).isoformat()

                insert_article(title, url, "HackerNews", "discussion", None, published_at)
            except Exception:
                continue
    except Exception as e:
        print(f"[HN Error]: {e}")


def fetch_reddit():
    try:
        resp = requests.get(REDDIT_URL, headers=HEADERS, timeout=10)
        data = resp.json()
        posts = data.get("data", {}).get("children", [])

        for post in posts:
            p = post.get("data", {})
            title = p.get("title", "").strip()
            url = p.get("url", "")
            permalink = p.get("permalink", "")
            selftext = (p.get("selftext") or "")[:300]

            if not url or url.startswith("/r/"):
                url = f"https://www.reddit.com{permalink}"

            published_at = None
            if p.get("created_utc"):
                published_at = datetime.fromtimestamp(p["created_utc"]).isoformat()

            if title and url:
                insert_article(title, url, "Reddit r/artificial", "discussion", selftext, published_at)
    except Exception as e:
        print(f"[Reddit Error]: {e}")


def fetch_all():
    for url, name, cat in RSS_FEEDS:
        fetch_rss(url, name, cat)
    fetch_hackernews()
    fetch_reddit()

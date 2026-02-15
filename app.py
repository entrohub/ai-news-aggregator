import threading
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_articles, get_sources
from fetcher import fetch_all
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
init_db()

# Auto-refresh every 2 days
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_all, "interval", days=2, id="auto_fetch")
scheduler.start()

TRANSLATIONS = {
    "zh": {
        "title": "AI 信息聚合器",
        "refresh": "刷新数据",
        "refreshing": "抓取中…",
        "search_placeholder": "搜索关键词…",
        "all_sources": "全部来源",
        "search_btn": "搜索",
        "results_count": "共 {} 条结果",
        "no_articles": "暂无文章",
        "no_articles_hint": "点击右上角「刷新数据」按钮抓取最新内容",
        "footer": "AI 信息聚合器 — 数据来自 ArXiv, HackerNews, Reddit 等公开源",
        "switch_lang": "EN",
        "switch_lang_code": "en",
    },
    "en": {
        "title": "AI News Aggregator",
        "refresh": "Refresh",
        "refreshing": "Fetching…",
        "search_placeholder": "Search keywords…",
        "all_sources": "All Sources",
        "search_btn": "Search",
        "results_count": "{} results",
        "no_articles": "No articles yet",
        "no_articles_hint": 'Click the "Refresh" button to fetch latest content',
        "footer": "AI News Aggregator — Data from ArXiv, HackerNews, Reddit and other public sources",
        "switch_lang": "中文",
        "switch_lang_code": "zh",
    },
}


@app.route("/")
def index():
    lang = request.args.get("lang", "zh")
    if lang not in TRANSLATIONS:
        lang = "zh"
    t = TRANSLATIONS[lang]

    source = request.args.get("source", "")
    query = request.args.get("q", "")
    articles = get_articles(source=source or None, query=query or None)
    sources = get_sources()
    return render_template("index.html", articles=articles, sources=sources,
                           current_source=source, current_query=query,
                           lang=lang, t=t)


@app.route("/refresh", methods=["POST"])
def refresh():
    lang = request.form.get("lang", "zh")
    # Run fetch in background thread to avoid request timeout
    threading.Thread(target=fetch_all, daemon=True).start()
    return redirect(url_for("index", lang=lang))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

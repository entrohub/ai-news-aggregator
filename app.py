from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_articles, get_sources
from fetcher import fetch_all

app = Flask(__name__)
init_db()


@app.route("/")
def index():
    source = request.args.get("source", "")
    query = request.args.get("q", "")
    articles = get_articles(source=source or None, query=query or None)
    sources = get_sources()
    return render_template("index.html", articles=articles, sources=sources,
                           current_source=source, current_query=query)


@app.route("/refresh", methods=["POST"])
def refresh():
    fetch_all()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

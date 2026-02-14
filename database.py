import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "articles.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            summary TEXT,
            published_at DATETIME,
            fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def insert_article(title, url, source, category="general", summary=None, published_at=None):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT OR IGNORE INTO articles (title, url, source, category, summary, published_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (title, url, source, category, summary, published_at),
        )
        conn.commit()
    finally:
        conn.close()


def get_articles(source=None, query=None):
    conn = get_connection()
    sql = "SELECT * FROM articles WHERE 1=1"
    params = []

    if source:
        sql += " AND source = ?"
        params.append(source)

    if query:
        sql += " AND (title LIKE ? OR summary LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])

    sql += " ORDER BY published_at DESC, fetched_at DESC LIMIT 200"

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def get_sources():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT source FROM articles ORDER BY source").fetchall()
    conn.close()
    return [r["source"] for r in rows]

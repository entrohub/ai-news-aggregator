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
            title_zh TEXT,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            summary TEXT,
            summary_zh TEXT,
            published_at DATETIME,
            fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add zh columns if upgrading from old schema
    for col in ("title_zh", "summary_zh"):
        try:
            conn.execute(f"ALTER TABLE articles ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()


def insert_article(title, url, source, category="general", summary=None,
                   published_at=None, title_zh=None, summary_zh=None):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT OR IGNORE INTO articles
               (title, title_zh, url, source, category, summary, summary_zh, published_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, title_zh, url, source, category, summary, summary_zh, published_at),
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
        sql += " AND (title LIKE ? OR summary LIKE ? OR title_zh LIKE ? OR summary_zh LIKE ?)"
        params.extend([f"%{query}%"] * 4)

    sql += " ORDER BY published_at DESC, fetched_at DESC LIMIT 200"

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def get_sources():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT source FROM articles ORDER BY source").fetchall()
    conn.close()
    return [r["source"] for r in rows]

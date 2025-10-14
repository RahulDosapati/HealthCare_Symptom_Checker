# backend/db.py
import sqlite3, os, json

DB_PATH = os.getenv("DB_PATH", "symptom_history.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        symptoms TEXT,
        response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_query(user_id, symptoms, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, symptoms, response) VALUES (?, ?, ?)",
              (user_id or "anonymous", symptoms, response))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT symptoms, response, created_at FROM history WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"symptoms": s, "response": r, "created_at": t} for s, r, t in rows]


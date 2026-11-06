
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "community.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                image TEXT,
                status TEXT DEFAULT 'Pending',
                admin_remarks TEXT,
                created_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

    print("CommunityConnect database initialized successfully!")


def create_user(name, email, password_hash):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )


def get_user_by_email(email):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()


def add_complaint(user_id, title, category, description,
                  location, image=None):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO complaints
            (user_id, title, category, description,
             location, image, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?)
        """, (
            user_id, title, category, description,
            location, image, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        return cursor.lastrowid


def get_user_complaints(user_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM complaints WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        ).fetchall()


def get_all_complaints():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM complaints ORDER BY id DESC"
        ).fetchall()


def update_complaint_status(complaint_id, status, remarks=""):
    with get_connection() as conn:
        conn.execute("""
            UPDATE complaints
            SET status = ?, admin_remarks = ?
            WHERE id = ?
        """, (status, remarks, complaint_id))


if __name__ == "__main__":
    init_db()

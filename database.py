
import sqlite3
from pathlib import Path
from datetime import datetime

# Database location
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "community.db"


def get_connection():
    """Connect to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the required database tables."""
    with get_connection() as conn:

        # Citizens table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'citizen'
            )
        """)

        # Complaints table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                image_path TEXT,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Pending',
                admin_remark TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)


def create_user(name, email, password_hash):
    """Register a new citizen."""
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO users (name, email, password_hash)
                VALUES (?, ?, ?)
            """, (name, email, password_hash))
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_email(email):
    """Find a citizen using their email."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()


def create_complaint(user_email, title, category,
                     description, location, image_path=None):
    """Submit a new community complaint."""
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO complaints (
                user_email, title, category, description,
                location, image_path, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_email,
            title,
            category,
            description,
            location,
            image_path,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        return cursor.lastrowid


def get_user_complaints(user_email):
    """Get complaints submitted by one citizen."""
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM complaints
            WHERE user_email = ?
            ORDER BY id DESC
        """, (user_email,)).fetchall()


def get_all_complaints():
    """Get all complaints for the admin dashboard."""
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM complaints
            ORDER BY id DESC
        """).fetchall()


def update_complaint_status(complaint_id, status, admin_remark=""):
    """Update complaint status and admin remark."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE complaints
            SET status = ?, admin_remark = ?
            WHERE id = ?
        """, (status, admin_remark, complaint_id))


# Initialize the database tables
if __name__ == "__main__":
    init_db()
    print("CommunityConnect database initialized successfully!")

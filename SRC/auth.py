import sqlite3
import hashlib
import secrets
from pathlib import Path
from datetime import datetime


# Database location
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "Database"
DATABASE_DIR.mkdir(exist_ok=True)

DB_PATH = DATABASE_DIR / "users.db"


# Connect to database
def get_connection():
    return sqlite3.connect(DB_PATH)


# Create users table
def init_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Hash password securely
def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return password_hash.hex(), salt.hex()


# Check password
def verify_password(password, stored_hash, stored_salt):
    salt = bytes.fromhex(stored_salt)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return secrets.compare_digest(
        password_hash.hex(),
        stored_hash
    )


# Register new user
def register_user(username, password):

    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    password_hash, salt = hash_password(password)

    try:
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO users
            (username, password_hash, salt, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                password_hash,
                salt,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    except Exception as e:
        return False, f"Error: {e}"


# Login user
def login_user(username, password):

    username = username.strip()

    conn = get_connection()

    user = conn.execute(
        """
        SELECT username, password_hash, salt
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    conn.close()

    if user is None:
        return False

    stored_username, stored_hash, stored_salt = user

    if verify_password(password, stored_hash, stored_salt):
        return True

    return False


# Initialize database automatically
init_database()
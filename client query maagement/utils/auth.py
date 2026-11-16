
import hashlib
from database.db import create_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password, role):

    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute("""
            INSERT INTO users (username, hashed_password, role)
            VALUES (?, ?, ?)
        """, (username, hashed_password, role))

        conn.commit()
        return True

    except Exception:
        return False

    finally:
        conn.close()


def login_user(username, password):

    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT username, role
        FROM users
        WHERE username = ? AND hashed_password = ?
    """, (username, hashed_password))

    user = cursor.fetchone()
    conn.close()

    return user

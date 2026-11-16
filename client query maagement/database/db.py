
import sqlite3
from datetime import datetime


def create_connection():
    return sqlite3.connect("database/client_queries.db")


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Queries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            query_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mail_id TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            query_heading TEXT NOT NULL,
            query_description TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            query_created_time TEXT NOT NULL,
            query_closed_time TEXT,
            category TEXT DEFAULT 'General Inquiry'
        )
    """)

    # Add category to existing database if missing
    cursor.execute("PRAGMA table_info(queries)")
    columns = [column[1] for column in cursor.fetchall()]

    if "category" not in columns:
        cursor.execute("""
            ALTER TABLE queries
            ADD COLUMN category TEXT DEFAULT 'General Inquiry'
        """)

    conn.commit()
    conn.close()


def insert_query(email, mobile, heading, description, category):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queries (
            mail_id,
            mobile_number,
            query_heading,
            query_description,
            status,
            query_created_time,
            category
        )
        VALUES (?, ?, ?, ?, 'Open', ?, ?)
    """, (
        email,
        mobile,
        heading,
        description,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        category
    ))

    conn.commit()
    conn.close()


def close_query(query_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE queries
        SET status = 'Closed',
            query_closed_time = ?
        WHERE query_id = ?
          AND status = 'Open'
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        query_id
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")


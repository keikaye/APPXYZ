"""
db.py — all the MySQL (XAMPP) plumbing lives here, kept separate from
app.py so the web-request logic stays easy to read.

XAMPP's MySQL defaults (unless you've changed them in the control panel):
  host     = 127.0.0.1
  port     = 3306
  user     = root
  password = ""   (blank)

NOTE: passwords are stored in PLAIN TEXT in the "password" column (no
hashing) — fine for this local school mockup where you want to be able to
open phpMyAdmin and see exactly what was typed, but never do this in a
real app with real users.
"""

import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "facebook_db",
}


def get_connection():
    """Open a fresh connection to the facebook_db database in XAMPP's MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


def find_user_by_identifier(identifier):
    """Look up a user row by their email or phone number. Returns a dict
    (e.g. {'id':1,'name':'Demo User','identifier':'demo@gmail.com',
    'password':'password123'}) or None if no such user exists."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM users WHERE identifier = %s", (identifier,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def create_user(name, identifier, password):
    """Insert a new user row (plain-text password). Raises
    mysql.connector.IntegrityError if the identifier already exists
    (it's a UNIQUE column)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, identifier, password) VALUES (%s, %s, %s)",
            (name, identifier, password),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

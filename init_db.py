"""
init_db.py — run this ONCE (python init_db.py) before starting app.py.

It talks to XAMPP's MySQL server to:
  1. Create the "facebook_db" database if it doesn't exist yet.
  2. (Re)create a "users" table with a PLAIN-TEXT "password" column.
  3. Seed the demo account (demo@gmail.com / password123).

Make sure MySQL is running in the XAMPP Control Panel before you run this.

NOTE: this version drops and recreates the "users" table (the column
changed from "password_hash" to plain "password"), so if you'd already
signed up real test accounts, they'll be cleared and reseeded with just
the demo account. Fine for a school mockup; just know it happens.
"""

import mysql.connector

DB_NAME = "facebook_db"
CONNECTION_ARGS = {"host": "127.0.0.1", "port": 3306, "user": "root", "password": ""}


def main():
    # Step 1: connect WITHOUT selecting a database yet, so we can create one.
    conn = mysql.connector.connect(**CONNECTION_ARGS)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    cur.close()
    conn.close()
    print(f"Database '{DB_NAME}' ready.")

    # Step 2: connect again, this time INTO that database, and (re)create the table.
    conn = mysql.connector.connect(database=DB_NAME, **CONNECTION_ARGS)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute(
        """
        CREATE TABLE users (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            name       VARCHAR(100) NOT NULL,
            identifier VARCHAR(100) NOT NULL UNIQUE,
            password   VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    print("Table 'users' (re)created with a plain-text 'password' column.")

    # Step 3: seed the demo account.
    cur.execute(
        "INSERT INTO users (name, identifier, password) VALUES (%s, %s, %s)",
        ("Demo User", "demo@gmail.com", "password123"),
    )
    conn.commit()
    print("Seeded demo account: demo@gmail.com / password123")

    cur.close()
    conn.close()
    print("All set. You can now run: python app.py")


if __name__ == "__main__":
    main()

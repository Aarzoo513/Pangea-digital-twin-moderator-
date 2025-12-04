import sqlite3
import os
from config import DATABASE_PATH, DATA_DIR


def init_database():
    """Initializes the SQLite DB only if it does NOT already exist."""

    # Ensure /data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Check if DB file already exists
    db_exists = os.path.isfile(DATABASE_PATH)

    # Create and connect to DB
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # If DB did not exist, create tables
    if not db_exists:
        print("Database not found. Creating a new one...")

        cursor.execute(
            """
            CREATE TABLE moderation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                answer TEXT,
                sexual INTEGER,
                hate_and_discrimination INTEGER,
                violence_and_threats INTEGER,
                dangerous_and_criminal_content INTEGER,
                selfharm INTEGER,
                health INTEGER,
                financial INTEGER,
                law INTEGER,
                pii INTEGER,
                risk_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        connection.commit()
        print("Database created successfully!")

    else:
        print("Database already exists. Nothing to do.")

    connection.close()
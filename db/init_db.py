import sqlite3
import os
from config import DATABASE_PATH, DATA_DIR


def init_database():
    # Crée le dossier /data si nécessaire
    os.makedirs(DATA_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Exemple de table (tu peux l’adapter)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS moderation_results (
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
    """)
          
    # Nouvelle table : rejected_prompts

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rejected_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    connection.commit()
    connection.close()
    print("Database initialized successfully !")

if __name__ == "__main__":
    init_database()

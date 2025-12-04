import sqlite3
from config import DATABASE_PATH


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
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
        """
    )

    conn.commit()
    conn.close()


def insert_empty_prompt_rows(prompt: str, count: int = 10):
    """Insert N empty rows with only the prompt filled."""
    conn = get_connection()
    cur = conn.cursor()

    for _ in range(count):
        cur.execute(
            """
            INSERT INTO moderation_results (prompt)
            VALUES (?)
            """,
            (prompt,),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    insert_empty_prompt_rows("how are you", count=10)
    print("✔️ 10 empty prompt rows inserted!")
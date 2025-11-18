import sqlite3
from config import DATABASE_PATH
from tabulate import tabulate


def get_connection():
    """Create and return a SQLite connection."""
    return sqlite3.connect(DATABASE_PATH)


def save_analysis(record: dict):
    """
    Save moderation analysis result into the database.
    """

    conn = get_connection()
    cur = conn.cursor()

    # 1) Find the next empty row (any prompt)
    cur.execute(
        """
        SELECT id, prompt
        FROM moderation_results
        WHERE (answer IS NULL OR answer = '')
          AND sexual IS NULL
          AND hate_and_discrimination IS NULL
          AND violence_and_threats IS NULL
          AND dangerous_and_criminal_content IS NULL
          AND selfharm IS NULL
          AND health IS NULL
          AND financial IS NULL
          AND law IS NULL
          AND pii IS NULL
          AND risk_score IS NULL
        ORDER BY id
        LIMIT 1
        """
    )

    row = cur.fetchone()

    if not row:
        conn.close()
        # You can log instead if you don't want an exception
        raise ValueError("No empty moderation_results row left to fill.")

    empty_id, prompt = row  # prompt is there if you want to log it

    # 2) Normalize values from `record`
    answer = record.get("answer")
    sexual = int(record.get("sexual", False))
    hate_and_discrimination = int(record.get("hate_and_discrimination", False))
    violence_and_threats = int(record.get("violence_and_threats", False))
    dangerous_and_criminal_content = int(record.get("dangerous_and_criminal_content", False))
    selfharm = int(record.get("selfharm", False))
    health = int(record.get("health", False))
    financial = int(record.get("financial", False))
    law = int(record.get("law", False))
    pii = int(record.get("pii", False))
    risk_score = record.get("risk_score", 0)

    # 3) Update that specific row
    cur.execute(
        """
        UPDATE moderation_results
        SET
            answer = ?,
            sexual = ?,
            hate_and_discrimination = ?,
            violence_and_threats = ?,
            dangerous_and_criminal_content = ?,
            selfharm = ?,
            health = ?,
            financial = ?,
            law = ?,
            pii = ?,
            risk_score = ?
        WHERE id = ?
        """,
        (
            answer,
            sexual,
            hate_and_discrimination,
            violence_and_threats,
            dangerous_and_criminal_content,
            selfharm,
            health,
            financial,
            law,
            pii,
            risk_score,
            empty_id,
        ),
    )

    conn.commit()
    conn.close()


def fetch_all():
    """Fetch all rows from the moderation_results table."""
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, prompt, answer, sexual, hate_and_discrimination, violence_and_threats, dangerous_and_criminal_content, selfharm, health, financial, law, pii, risk_score, created_at FROM moderation_results;")
    rows = cur.fetchall()

    headers = ["id", "prompt", "answer", "sexual", "hate_and_discrimination", "violence_and_threats",
                "dangerous_and_criminal_content", "selfharm", "health", "financial", "law", "pii",
                    "risk_score", "created_at"]
    return tabulate(rows, headers=headers, tablefmt="grid")
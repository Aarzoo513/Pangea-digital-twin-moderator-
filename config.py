import os
from dotenv import load_dotenv
from pathlib import Path

PROJECT_DIR = Path(__file__).parent

# Explicit path to .env in the same folder as config.py
ENV_PATH = PROJECT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# ---- API KEYS ----
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ---- PATHS ----
DATA_DIR = PROJECT_DIR / "data"
DATABASE_PATH = DATA_DIR / "database.db"

# ---- MODEL CONFIG ----
MODERATION_MODEL = "mistral-moderation-latest"

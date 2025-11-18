import os
from dotenv import load_dotenv
from pathlib import Path

PROJECT_DIR = Path(__file__).parent

# Load environment variables (.env)
load_dotenv()

# ---- API KEYS ----
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ---- PATHS ----
DATA_DIR = PROJECT_DIR / "data"
DATABASE_PATH = DATA_DIR / "database.db"

# ---- MODEL CONFIG ----
MODERATION_MODEL = "mistral-moderation-latest"

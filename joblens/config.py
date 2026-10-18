import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_PATH = BASE_DIR / "data" / "db" / "jobs.db"

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"
NINJA_URL = "https://api.openwebninja.com/jsearch/search-v2"
NINJA_API_KEY = os.getenv("X-API-Key")
NINJA_QUERIES = ["data scientist"]

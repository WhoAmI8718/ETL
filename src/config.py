import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent

DATA_FILE = BASE_DIR / "data" / "products_10x10.csv"

ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

DB_CONNECTION = os.getenv("DB_CONNECTION")

if DB_CONNECTION is None:
    raise RuntimeError("DB_CONNECTION не найдена в .env")
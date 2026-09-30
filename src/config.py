import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "products_10x10.csv"
ENV_FILE = BASE_DIR / ".env"


def get_local_db_connection() -> str:
    load_dotenv(ENV_FILE)

    db_connection = os.getenv("DB_CONNECTION")

    if db_connection is None:
        raise RuntimeError(
            "DB_CONNECTION не найдена в .env"
        )

    return db_connection
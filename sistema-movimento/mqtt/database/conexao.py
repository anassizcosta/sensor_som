import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


def conectar_banco():
    url = os.getenv("DATABASE_URL")

    if not url:
        raise ValueError(
            f"DATABASE_URL não encontrada. Verifique o arquivo: {ENV_FILE}"
        )

    return psycopg2.connect(url)
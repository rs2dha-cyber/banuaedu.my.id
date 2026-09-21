import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "ganti-dengan-secret-key-anda")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + str(BASE_DIR / "instance" / "banua_edu.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

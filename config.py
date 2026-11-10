import os
from datetime import timedelta

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER", "academie_app"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "academie_diplomatie"),
    ).render_as_string(hide_password=False)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookies de session et "Se souvenir de moi"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    # Le jeton CSRF expire avec la session (évite les erreurs sur une page restée ouverte)
    WTF_CSRF_TIME_LIMIT = None

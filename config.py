import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-jangan-dipakai-produksi")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "instance", "portfolio.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "images", "projects")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024


os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
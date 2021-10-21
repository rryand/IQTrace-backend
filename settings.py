import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
API_URL = os.environ.get("API_URL")

SMTP_PORT = int(os.environ.get("SMTP_PORT"))
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
EMAIL_PASSWORD = os.environ.get("SENDER_EMAIL_PASSWORD")

ALLOWED_MIME_TYPES = ["image/png", "image/jpeg"]

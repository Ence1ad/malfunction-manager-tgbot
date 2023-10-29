import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
SECRET_KEY = os.getenv("SECRET_KEY")

POSTGRES_USER = str(os.getenv("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
POSTGRES_DB = str(os.getenv("POSTGRES_DB"))
SQL_HOST = str(os.getenv("SQL_HOST"))
PORT = str(os.getenv("PORT"))

admins = [
    os.getenv("ADMIN_ID")
]

ip = os.getenv("DJANGO_ALLOWED_HOSTS")

POSTGRES_URL = f"postgres+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{SQL_HOST}:{PORT}/{POSTGRES_DB}"

chat_id_group = os.getenv("CHAT_ID")

PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")


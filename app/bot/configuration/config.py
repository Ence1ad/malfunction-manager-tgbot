import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
# BASE_URL = 'https://example.com'  # Webhook domain
# WEBHOOK_PATH = f'/tg/webhooks/bot/{BOT_TOKEN}'
# WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'

SECRET_KEY = os.getenv("SECRET_KEY")

PGUSER = str(os.getenv("PGUSER"))
POSTGRES_PASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
DBHOST = str(os.getenv("DBHOST"))
PORT = str(os.getenv("PORT"))

admins = [
    os.getenv("ADMIN_ID")
]

ip = os.getenv("DJANGO_ALLOWED_HOSTS")

POSTGRES_URL = f"postgres://{PGUSER}:{POSTGRES_PASSWORD}@{DBHOST}:{PORT}/{DATABASE}"

chat_id_group = os.getenv("CHAT_ID")

PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")


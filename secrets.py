import os

TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
print(TOKEN)
API_URL = os.environ.get("TELEGRAM_API_URL")
RABBIT_URL = os.environ.get("RABBIT_URL")
REDIS_URL = os.environ.get("REDIS_URL")
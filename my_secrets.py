import os

LOG_LEVEL = 1

MAIN_CHANNEL_ANCHOR_MESSAGE: int = int(os.environ["TELEGRAM_MAIN_CHANNEL_ANCHOR_MESSAGE"])
API_URL: str = os.environ.get("TELEGRAM_API_URL") or "http://127.0.0.1:8000/api/v1/"
DEBUG_CHANNEL: str = os.environ.get("TELEGRAM_DEBUG_CHANNEL") or '-1002121702897'
MAIN_CHANNEL: str = os.environ["TELEGRAM_MAIN_CHANNEL"]
TOKEN: str = os.environ["TELEGRAM_API_TOKEN"]

CHECK_ZAMENA_INTERVAL_START_HOUR: str | None = os.environ.get("CHECK_ZAMENA_INTERVAL_START_HOUR")
CHECK_ZAMENA_INTERVAL_END_HOUR: str | None = os.environ.get("CHECK_ZAMENA_INTERVAL_END_HOUR")
CHECK_ZAMENA_INTERVAL_MINUTES: str | None = os.environ.get("CHECK_ZAMENA_INTERVAL_MINUTES")

SCHEDULER_SUPABASE_ANON_KEY: str = os.environ["SCHEDULER_SUPABASE_ANON_KEY"]
SCHEDULER_SUPABASE_URL: str = os.environ["SCHEDULER_SUPABASE_URL"]

BACKEND_URL: str | None = os.environ.get("BACKEND_URL")
RABBIT_URL: str | None = os.environ.get("RABBIT_URL")
BROKER_URL: str | None = os.environ.get("BROKER_URL")
REDIS_URL: str | None = os.environ.get("REDIS_URL")
API_KEY: str = os.environ["API_KEY"]
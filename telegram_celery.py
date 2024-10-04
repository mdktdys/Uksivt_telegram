from celery import Celery

from secrets import BROKER_URL, BACKEND_URL
import celery_pool_asyncio

telegram_celery_app = Celery(
    "telegram_bot",
    broker=BROKER_URL,
    backend=BACKEND_URL,
)

telegram_celery_app.autodiscover_tasks(packages=["telegram"], force=True)

print("***")
print(telegram_celery_app.tasks.keys())
print("***")

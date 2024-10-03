import asyncio
import datetime
import html
import traceback
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

admins = [1283168392]


@router.message(F.text, Command("latest"))
async def my_handler(message: Message):
    try:
        # Lazy import inside the function
        from telegram import telegram_celery_app

        # Отправляем задачу с использованием delay()
        task = telegram_celery_app.send_task("parser.tasks.get_latest_zamena_link").delay()

        # Функция для периодической проверки статуса задачи
        async def check_task_result():
            while not task.ready():
                await asyncio.sleep(1)  # Ждем 1 секунду перед следующей проверкой
            return task.result  # Возвращаем результат, когда задача завершена

        # Запускаем проверку в отдельной задаче
        task_result = await check_task_result()

        await message.answer(f"{task_result}")
    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message
        await send_error_message(
            bot=message.bot,
            chat_id=message.chat.id,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )


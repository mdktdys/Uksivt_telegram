import asyncio
import datetime
import html
import traceback
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from celery.result import AsyncResult

router = Router()

admins = [1283168392]

from your_celery_app import get_latest_zamena_link  # Импортируйте вашу задачу
import asyncio


@router.message(F.text, Command("latest"))
async def my_handler(message: Message):
    try:
        chat_id = message.chat.id
        # Отправляем задачу с использованием delay()
        task = get_latest_zamena_link.delay()  # Вызываем delay() на задаче

        # Функция для периодической проверки статуса задачи
        async def check_task_result(task_id):
            result = AsyncResult(task_id)  # Создаем AsyncResult для проверки
            while not result.ready():
                await asyncio.sleep(1)  # Ждем 1 секунду перед следующей проверкой
            return result.result  # Возвращаем результат, когда задача завершена

        # Запускаем проверку в отдельной задаче
        task_result = await check_task_result(task.id)

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



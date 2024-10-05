import asyncio
import datetime
import html
import traceback
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from secrets import DEBUG_CHANNEL

router = Router()

admins = [1283168392]


from celery.result import AsyncResult


@router.message(F.text, Command("latest"))
async def my_handler(message: Message):
    from utils.sender import send_error_message

    max_retries = 5  # Максимальное количество попыток
    retries = 0  # Счетчик попыток

    try:
        chat_id = message.chat.id

        # Lazy import inside the function
        from telegram_celery import telegram_celery_app

        while retries < max_retries:
            # Отправляем таску и сохраняем ID
            task = telegram_celery_app.send_task(
                "parser.tasks.get_latest_zamena_link", args=[]
            )
            task_id = task.id

            # Ожидаем выполнения таски
            result = AsyncResult(task_id)

            # Ожидаем, пока таска выполнится
            while not result.ready():
                await asyncio.sleep(1)  # Спим, чтобы не перегружать CPU

            if result.successful():
                task_result = result.result  # Получаем результат таски
                link = task_result["link"]
                date = task_result["date"]
                await message.answer(f"{date}\n{link}")
                return
            elif result.failed():
                retries += 1  # Увеличиваем счетчик попыток
                await message.answer(
                    f"Неудачная доставка. Попытка {retries}/{max_retries}"
                )

                # Если достигнут лимит попыток, отправляем сообщение об ошибке
                if retries == max_retries:
                    await message.answer("Достигнут лимит попыток. Попробуйте позже.")
                    error_body = f"{result.traceback}"
                    await send_error_message(
                        bot=message.bot,
                        chat_id=DEBUG_CHANNEL,
                        error_header="Ошибка",
                        application="Kronos",
                        time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
                        error_body=error_body,
                    )
                    return
            else:
                await send_error_message(
                    bot=message.bot,
                    chat_id=DEBUG_CHANNEL,
                    error_header="Ошибка",
                    application="Kronos",
                    time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
                    error_body="Я где-то проебал задачу, но получил её",
                )
                return

    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"

        await send_error_message(
            bot=message.bot,
            chat_id=DEBUG_CHANNEL,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )


@router.message(F.text, Command("check"))
async def my_handler(message: Message):
    try:
        # Lazy import inside the function
        from telegram_celery import telegram_celery_app

        telegram_celery_app.send_task("parser.tasks.check_new", args=[])
    except Exception as e:
        error_body = f"{str(e)}\n\n{traceback.format_exc()}"
        from utils.sender import send_error_message

        await send_error_message(
            bot=message.bot,
            chat_id=DEBUG_CHANNEL,
            error_header="Ошибка",
            application="Kronos",
            time_=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p"),
            error_body=error_body,
        )

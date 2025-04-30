from aiogram import Bot


async def send_large_text(bot: Bot, chat_id: int | str, text: str, max_length: int = 4096):
    """
    Отправляет большой текст, разбивая его на части, если он превышает максимальную длину сообщения.

    :param bot: Экземпляр бота.
    :param chat_id: ID чата, в который нужно отправить сообщение.
    :param text: Текст, который нужно отправить.
    :param max_length: Максимальная длина одного сообщения (по умолчанию 4096 символов).
    """
    while len(text) > max_length:
        # Находим последний пробел перед max_length, чтобы не разрезать слова
        part = text[:max_length]
        last_space = part.rfind(" ")
        if last_space != -1:
            part = part[:last_space]

        await bot.send_message(chat_id, part)
        text = text[
            len(part) :
        ].lstrip()  # Убираем отправленную часть и лидирующие пробелы

    if text:
        await bot.send_message(chat_id, text)

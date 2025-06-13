from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.schedule_api import ScheduleApi
from models.teacher_model import Teacher
from models.queue_model import Queue
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


router = Router(name = 'queues_router')

@router.callback_query(F.data.startswith('teacher_queues'))
async def show_teacher_queues(callback: CallbackQuery, api: ScheduleApi) -> None:
    teacher_id: str = callback.data.split('|')[1]
    teacher: Teacher | None = await api.get_teacher(teacher_id = teacher_id)
    
    if teacher is None:
        return
    
    queues: list[Queue] = await api.get_teacher_queues(teacher_id = teacher_id)
    lines = []
    for queue in queues:
        button_text: str = f'{queue.name}'
        lines.append([InlineKeyboardButton(text= button_text, callback_data = f'queue|{queue.id}')])
    
    lines.append([InlineKeyboardButton(text = 'Назад', callback_data = f'teacher|{teacher.id}')])
    
    text = 'Очереди преподавателя {teacher.name}'
    callback.bot.edit_message_text(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        text = text,
        reply_markup = InlineKeyboardMarkup(inline_keyboard = lines)
    )
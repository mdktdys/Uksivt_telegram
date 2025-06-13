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
    
    text: str = f'Очереди преподавателя {teacher.name}'
    await callback.bot.edit_message_text(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        text = text,
        reply_markup = InlineKeyboardMarkup(inline_keyboard = lines)
    )
    

@router.callback_query(F.data.startswith('queue'))
async def show_queue(callback: CallbackQuery, api: ScheduleApi) -> None:
    queue_id: str = callback.data.split('|')[1]
    queue: Queue | None = await api.get_queue(queue_id = queue_id)
    
    if queue is None:
        return
    
    lines = []
    for entry in queue.students:
        lines.append(f'#{entry.position} {entry.student}')
    
    body = '\n'.join(lines)
    text: str = f'''
Очередь {queue.name}

{body}
'''

    buttons: list[InlineKeyboardButton] = []
    if callback.message.chat.type == 'private':
        contains_me: bool = any([True if student.student == callback.from_user.id else False for student in queue.students])
        if contains_me:
            buttons.append([InlineKeyboardButton(text = 'Занять', callback_data = f'add_to_queue|{queue.id}|{callback.from_user.id}')])
        else:
            buttons.append([InlineKeyboardButton(text = 'Выйти', callback_data = f'remove_from_queue|{queue.id}|{callback.from_user.id}')]) 
    
    buttons.append([InlineKeyboardButton(text = 'Назад', callback_data = f'teacher_queues|{queue.teacher}')])
    await callback.bot.edit_message_text(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        text = text,
        reply_markup = InlineKeyboardMarkup(inline_keyboard = buttons)
    )
    

@router.callback_query(F.data.startswith('add_to_queue'))
async def add_to_queue(callback: CallbackQuery, api: ScheduleApi) -> None:
    data: list[str] = callback.data.split('|')
    queue_id: str = data[1]
    user_id: str = data[2]
    await api.add_to_queue(queue_id = queue_id, user_id = user_id)
    await show_queue(callback = callback, api = api)
    

@router.callback_query(F.data.startswith('remove_from_queue'))
async def remove_from_queue(callback: CallbackQuery, api: ScheduleApi) -> None:
    data: list[str] = callback.data.split('|')
    queue_id: str = data[1]
    user_id: str = data[2]
    await api.remove_from_queue(queue_id = queue_id, user_id = user_id)
    await show_queue(callback = callback, api = api)
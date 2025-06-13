import datetime
import json
import logging
import aiohttp
from models.search_result import DayScheduleFormatted
from models.teacher_model import Teacher
from models.queue_model import Queue
from models.add_to_queue_model import AddQueueEntryForm


class ScheduleApi:
    def __init__(self, api_key: str, api_url: str) -> None:
        self.api_key: str = api_key
        self.api_url: str = api_url
        self.headers: dict[str, str] = {
            "X-API-KEY": self.api_key
        }

    async def get_group_schedule_formatted(self, group: str, date: datetime.date, chat_id: int) -> DayScheduleFormatted:
        async with aiohttp.ClientSession(trust_env=True) as session:
            url: str = ApiRoutes.GROUP_SCHEDULE_FORMATTED.format(group=group, date=date, chat_id=chat_id, api_url=self.api_url)
            async with session.get(url, headers = self.headers) as res:
                if res.status != 200:
                    logging.error(f"Failed to get group schedule formatted from {url}: {await res.text()}")
                    raise Exception("Failed to get group schedule formatted")

                response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(await res.text())
                return response
            
    
    async def get_teacher(self, teacher_id: int) -> Teacher:
        async with aiohttp.ClientSession(trust_env=True) as session:
            url: str = ApiRoutes.get_teacher.format(id = teacher_id, api_url=self.api_url)
            async with session.get(url) as res:
                if res.status != 200:
                    raise Exception('failed get teacher')

                raw_json = await res.text()
                parsed = json.loads(raw_json)
                return [Teacher.model_validate(item) for item in parsed][0]
            
    
    async def get_teacher_queues(self, teacher_id: int) -> list[Queue]:
        async with aiohttp.ClientSession(trust_env=True) as session:
            url: str = ApiRoutes.get_teacher_queues.format(teacher_id = teacher_id, api_url=self.api_url)
            async with session.get(url) as res:
                if res.status != 200:
                    raise Exception('failed get teacher')

                raw_json = await res.text()
                parsed = json.loads(raw_json)
                return [Queue.model_validate(item) for item in parsed]
            
    
    async def get_queue(self, queue_id: int) -> Queue:
        async with aiohttp.ClientSession(trust_env=True) as session:
            url: str = ApiRoutes.get_queue.format(queue_id = queue_id, api_url=self.api_url)
            async with session.get(url) as res:
                if res.status != 200:
                    raise Exception('failed get teacher')

                return Queue.model_validate_json(await res.text())


    async def add_to_queue(self, queue_id: int, user_id: str, form: AddQueueEntryForm):
        async with aiohttp.ClientSession(trust_env=True) as session:
            url: str = ApiRoutes.get_queue.format(queue_id = queue_id, api_url = self.api_url)
            async with session.post(url, json = form.model_dump()) as res:
                if res.status != 200:
                    raise Exception('failed get teacher')

                return None


    async def remove_from_queue(self, entry_id: int, user_id: str):
        async with aiohttp.ClientSession(trust_env=True) as session:
            url: str = ApiRoutes.get_queue.format(queue_id = entry_id, api_url = self.api_url)
            async with session.delete(url) as res:
                if res.status != 200:
                    raise Exception('failed get teacher')

                return None


class ApiRoutes:
    GROUP_SCHEDULE_FORMATTED = "{api_url}groups/day_schedule_formatted/{group}/{date}/{chat_id}/"
    get_teacher: str = "{api_url}teachers/id/{id}/"
    get_teacher_queues: str = "{api_url}teachers/queues/{teacher_id}/"
    get_queue: str = "{api_url}teachers/queue/{queue_id}/"

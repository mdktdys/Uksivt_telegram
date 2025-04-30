import datetime
import logging
import aiohttp
from models.search_result import DayScheduleFormatted
from my_secrets import API_URL


class ScheduleApi:
    def __init__(self, api_key: str, api_url: str) -> None:
        self.api_key: str = api_key
        self.api_url: str = api_url

    async def get_group_schedule_formatted(self, group: str, date: datetime.date, chat_id: int) -> DayScheduleFormatted:
        async with aiohttp.ClientSession(trust_env=True) as session:
            url: str = ApiRoutes.GROUP_SCHEDULE_FORMATTED.format(group=group, date=date, chat_id=chat_id, api_url=self.api_url)
            logging.debug(f"Getting group schedule formatted from {url}")
            async with session.get(url, headers={"X-API-KEY": self.api_key}) as res:
                if res.status != 200:
                    logging.error(f"Failed to get group schedule formatted from {url}: {await res.text()}")
                    raise Exception("Failed to get group schedule formatted")

                response: DayScheduleFormatted = DayScheduleFormatted.model_validate_json(await res.text())
                return response


class ApiRoutes:
    GROUP_SCHEDULE_FORMATTED = "{api_url}groups/day_schedule_formatted/{group}/{date}/{chat_id}/"


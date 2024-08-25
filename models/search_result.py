from typing import List

from pydantic import BaseModel, ConfigDict, ValidationError


class DayScheduleFormatted(BaseModel):
    model_config = ConfigDict(strict=True)
    paras: List[str]
    search_name: str

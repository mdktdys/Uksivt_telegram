from typing import List

from pydantic import BaseModel, ConfigDict, ValidationError


class DayScheduleFormatted(BaseModel):
    model_config = ConfigDict(strict=True)
    paras: List[str]
    full_zamena: bool
    search_name: str

from pydantic import BaseModel, ConfigDict, Field
from datetime import time


class Timings(BaseModel):
    model_config = ConfigDict(strict=True)
    
    number: int
    start: time 
    end: time
    saturday_start: time = Field(alias = 'saturdayStart')
    saturday_end: time = Field(alias = 'saturdayEnd')
    obed_start: time = Field(alias = 'obedStart')
    obed_end: time = Field(alias = 'obedEnd')
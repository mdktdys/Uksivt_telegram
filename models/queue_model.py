from pydantic import BaseModel


class Queue(BaseModel):
    id: int
    teacher: int
    name: str
from pydantic import BaseModel


class Teacher(BaseModel):
    id: int
    name: str
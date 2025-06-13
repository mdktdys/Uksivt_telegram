from pydantic import BaseModel

    

class QueueEntry(BaseModel):
    id: int
    queue: int
    position: int
    student: str
    comment: str
    teacher_comment: str | None


class Queue(BaseModel):
    id: int
    teacher: int
    name: str
    students: list[QueueEntry] = []
from pydantic import BaseModel

    

class QueueEntry(BaseModel):
    id: int
    queue: int
    position: int
    student: str
    comment: str
    creator_tg_id: str
    teacher_comment: str | None


class Queue(BaseModel):
    id: int
    teacher: int
    name: str
    students: list[QueueEntry] = []
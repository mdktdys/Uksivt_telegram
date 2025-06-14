from pydantic import BaseModel, ConfigDict


class AddQueueEntryForm(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    queue_id: int
    position: int
    student: str
    creator_tg_id: str
    comment: str

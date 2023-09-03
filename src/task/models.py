import datetime
from pydantic import (
    BaseModel,
    Field
)


class TaskBase(BaseModel):
    event_type: str
    meta: dict | None


class Task(TaskBase):
    event_time: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

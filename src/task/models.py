import datetime
from pydantic import (
    BaseModel,
    Field
)


class Task(BaseModel):
    event_type: str
    event_time: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    meta: dict | None

from src.task.models import (
    Task,
    TaskBase
)
from pydantic_factories import ModelFactory

class TaskFactory(ModelFactory):
    __model__ = Task

class TaskBaseFactory(ModelFactory):
    __model__ = TaskBase


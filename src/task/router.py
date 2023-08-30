from dependency_injector.wiring import (
    Provide,
    inject
)
from fastapi import (
    APIRouter,
    Depends
)
from src.task.models import Task
from src.task.queue import KafkaClient
from src.task.container import TaskContainer


task_router = APIRouter()


@task_router.get("/task")
@inject
async def get_task(
    handler: KafkaClient = Depends(Provide[TaskContainer.kafka_client])
) -> Task:
    return handler.get_task()


@task_router.post("/task")
@inject
async def post_task(
    task: Task,
    handler: KafkaClient = Depends(Provide[TaskContainer.kafka_client])
) -> None:
    handler.produce_task(task=task)

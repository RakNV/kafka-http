from dependency_injector.wiring import (
    Provide,
    inject
)
from fastapi import (
    APIRouter,
    Depends
)
from loguru import logger
from src.task.models import (
    Task,
    TaskBase
)
from src.task.handler import Handler
from src.task.container import TaskContainer


task_router = APIRouter()


@task_router.get("/task/peek")
@inject
async def get_task(
    handler: Handler = Depends(Provide[TaskContainer.handler])
) -> Task | None:
    return handler.get_task()


@task_router.put("/task")
@inject
async def put_task(
    handler: Handler = Depends(Provide[TaskContainer.handler])
) -> Task:
    return handler.put_task()


@task_router.post("/task")
@inject
async def post_task(
    task: TaskBase,
    handler: Handler = Depends(Provide[TaskContainer.handler])
) -> None:
    logger.debug(type(task))
    handler.produce_task(task=task)


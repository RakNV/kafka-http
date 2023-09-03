from dependency_injector.wiring import (
    Provide,
    inject
)
from fastapi import (
    APIRouter,
    Depends
)
from src.task.models import (
    Task,
    TaskBase
)
from src.task.handler import Handler
from src.task.container import TaskContainer


task_router = APIRouter()


@task_router.get("/task")
@inject
async def get_task(
    handler: Handler = Depends(Provide[TaskContainer.handler])
) -> Task:
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
    handler.produce_task(task=task)


@task_router.get("/task/all")
@inject
async def get_all_tasks(
    handler: Handler = Depends(Provide[TaskContainer.handler])
) -> list[Task]:
    return handler.get_all_tasks()

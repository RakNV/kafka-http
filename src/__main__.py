from collections.abc import Callable
import uvicorn  # type: ignore
from fastapi import (
    Request,
    Response,
)
from loguru import logger
from .container import Application
from src.task.router import task_router

application_container = Application()
fastapi_app = application_container.fastapi_app()


@fastapi_app.middleware("http")
async def log_middle(request: Request, call_next: Callable) -> Response:
    url = "/" + str(request.url).removeprefix(str(request.base_url))
    logger.info(f"Request: {request.method} {url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} {url}")
    return response


fastapi_app.include_router(
    task_router,
    tags=["task"]
)


def run() -> None:
    uvicorn.run(
        "src.__main__:fastapi_app",
        host=application_container.config.service.address(),  # type: ignore
        port=application_container.config.service.port(),  # type: ignore
        loop="uvloop",
    )

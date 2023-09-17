from fastapi.exceptions import HTTPException
from .models import (
    Task,
    TaskBase
)
from .queue import (
    ConsumerClient, 
    ProducerClient
)


class Handler:

    def __init__( self,
        consumer_client: ConsumerClient,
        producer_client: ProducerClient,
    ) -> None:
        self.__consumer_client = consumer_client
        self.__producer_client = producer_client

    def get_task(self) -> Task | None:
        try:
            task = self.__consumer_client.get_task()
            return task
        except IndexError:
            raise HTTPException(
                status_code=404,
                detail={"message": "Task queue is empty", "code": 404}
            )

    def put_task(self) -> Task:
        try:
            return self.__consumer_client.put_task()
        except IndexError:
            raise HTTPException(
                status_code=404,
                detail={"message": "Task queue is empty", "code": 404}
                ) 

    def produce_task(self, task: TaskBase) -> None:
        return self.__producer_client.produce_task(
            task=Task(
                event_type=task.event_type,
                meta=task.meta
            )
        )

    def get_all_tasks(self) -> list[Task]:
        return self.__consumer_client.get_all_tasks()

from .models import (
    Task,
    TaskBase
)
from .queue import (
    ConsumerClient,
    ProducerClient
)


class Handler:

    def __init__(
        self,
        consumer_client_get: ConsumerClient,
        consumer_client_put: ConsumerClient,
        producer_client: ProducerClient
    ) -> None:
        self.__consumer_client_get = consumer_client_get
        self.__consumer_client_put = consumer_client_put
        self.__producer_client = producer_client

    def get_task(self) -> Task:
        return self.__consumer_client_get.get_task(delete=False)

    def put_task(self) -> Task:
        return self.__consumer_client_put.get_task(delete=True)

    def produce_task(self, task: TaskBase) -> None:
        return self.__producer_client.produce_task(task=Task(**task.dict()))

    def get_all_tasks(self) -> list[Task]:
        return self.__consumer_client_get.get_all_tasks()

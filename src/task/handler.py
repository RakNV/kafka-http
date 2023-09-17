from .models import (
    Task,
    TaskBase
)
from .queue import (
    ConsumerClient, 
    ProducerClient
)
from .decorator import handle_error
from .errors import QUEUE_IS_EMPTY_ERROR


class Handler:

    def __init__( self,
        consumer_client: ConsumerClient,
        producer_client: ProducerClient,
    ) -> None:
        self.__consumer_client = consumer_client
        self.__producer_client = producer_client

    @handle_error(
        beware=IndexError, 
        panic=QUEUE_IS_EMPTY_ERROR
    )
    def get_task(self) -> Task | None:
            return self.__consumer_client.get_task()

    @handle_error(
        beware=IndexError,
        panic=QUEUE_IS_EMPTY_ERROR
    )
    def put_task(self) -> Task:
        return self.__consumer_client.put_task()

    def produce_task(self, task: TaskBase) -> None:
        return self.__producer_client.produce_task(
            task=Task(
                event_type=task.event_type,
                meta=task.meta
            )
        )


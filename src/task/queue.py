import json
from loguru import logger
from kafka import (
    KafkaConsumer,
    KafkaProducer, 
)
from .models import Task
from .decorator import remember, sync


_IN_MEMORY_QUEUE = []


class ProducerClient:

    def __init__(
        self,
        producer: KafkaProducer,
        topic_name: str,
    ) -> None:
        self.__producer = producer
        self.__topic_name = topic_name

    @remember(queue_instance=_IN_MEMORY_QUEUE)
    def produce_task(self, task: Task) -> None:
            self.__handle_task(task=task)

    def __handle_task(self, task: Task) -> None:
        logger.debug(
            f"Sending event {task.json()} to {self.__topic_name} Kafka Topic...")
        self.__producer.send(self.__topic_name, json.loads(task.json()))
        logger.debug("Succeeded sending event")


class ConsumerClient:

    def __init__(
        self,
        consumer: KafkaConsumer,
    ) -> None:
        self.__consumer = consumer

    def get_task(self) -> Task | None:
        return _IN_MEMORY_QUEUE[0]

    @sync(queue_instance=_IN_MEMORY_QUEUE)
    def put_task(self):
        message = next(self.__consumer)
        self.__consumer.commit()  # Commit the offset to advance to the next message
        return Task(**message.value)

    def get_all_tasks(self) -> list[Task]:
        return [Task(**message.value) for message in self.__consumer]

    def __get_task(self, delete: bool) -> Task:
        logger.debug("Attempt to get task from consumer")
        message = next(self.__consumer)
        if delete:
            self.__consumer.commit()
        return Task(**message.value)

import json
from loguru import logger
from kafka import (
    KafkaConsumer,
    KafkaProducer
)
from .models import (
    Task,
    TaskBase
)


class ProducerClient:

    def __init__(
        self,
        producer: KafkaProducer,
        topic_name: str
    ) -> None:
        self.__producer = producer
        self.__topic_name = topic_name

    def produce_task(self, task: TaskBase) -> None:
        logger.debug(f"Sending event {task.json()} to {self.__topic_name} Kafka Topic...")
        self.__producer.send(self.__topic_name, json.loads(task.json()))
        logger.debug("Succeeded sending event")


class ConsumerClient:

    def __init__(
        self,
        consumer: KafkaConsumer,
    ) -> None:
        self.__consumer = consumer

    def get_task(self, delete: bool) -> Task:
        return self.__get_task(delete=delete)

    def get_all_tasks(self) -> list[Task]:
        return [Task(**message.value) for message in self.__consumer]

    def __get_task(self, delete: bool) -> Task:
        logger.debug("Attempt to get task from consumer")
        message = next(self.__consumer)
        if delete:
            self.__consumer.commit()
        return Task(**message.value)

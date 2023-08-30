import json
from loguru import logger
from kafka import (
    KafkaConsumer,
    KafkaProducer
)
from .models import Task


class KafkaClient:

    def __init__(
        self,
        consumer: KafkaConsumer,
        producer: KafkaProducer,
        topic_name: str
    ) -> None:
        self.__producer = producer
        self.__consumer = consumer
        self.__topic_name = topic_name

    def get_task(self) -> Task:
        task = self.__get_task()
        while not task:
            task = self.__get_task()
        return task

    def __get_task(self) -> Task:
        logger.debug("Attempt to get task from consumer")
        for message in self.__consumer:
            return Task(**message.value)

    def produce_task(self, task: Task) -> None:
        logger.debug(f"Sending event {task.json()} to {self.__topic_name} Kafka Topic...")
        self.__producer.send(self.__topic_name, json.loads(task.json()))
        logger.debug("Succeeded sending event")

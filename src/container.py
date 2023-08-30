import json

from fastapi import FastAPI
from kafka import (
    KafkaConsumer,
    KafkaProducer
)
from dependency_injector import (
    containers,
    providers
)
from src.config.container import Configuration
from src.task.container import TaskContainer


class Application(containers.DeclarativeContainer):
    config = providers.Container(Configuration)

    kafka_consumer = providers.Singleton(
        KafkaConsumer,
        config.kafka.task_topic(),
        bootstrap_servers=config.kafka.bootstrap_servers(),
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id=config.kafka.group_id(),
        consumer_timeout_ms=config.kafka.consumer_timeout(),
        enable_auto_commit=True,
        auto_offset_reset="earliest"
    )
    kafka_producer: KafkaProducer = providers.Singleton(
        KafkaProducer,
        bootstrap_servers=config.kafka.bootstrap_servers(),
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    fastapi_app = providers.Singleton(FastAPI)

    task = providers.Container(
        TaskContainer,
        kafka_producer=kafka_producer,
        kafka_consumer=kafka_consumer,
        topic_name=config.kafka.task_topic()
    )

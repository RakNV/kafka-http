from dependency_injector import (
    containers,
    providers
)
from .queue import KafkaClient


class TaskContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".router"])

    kafka_producer = providers.Dependency()
    kafka_consumer = providers.Dependency()
    topic_name = providers.Dependency()

    kafka_client = providers.Singleton(
        KafkaClient,
        consumer=kafka_consumer,
        producer=kafka_producer,
        topic_name=topic_name
    )

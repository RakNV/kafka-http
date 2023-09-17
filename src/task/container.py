from dependency_injector import (
    containers,
    providers
)
from .queue import (
    ConsumerClient,
    ProducerClient
)
from .handler import Handler


class TaskContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".router"])

    kafka_producer = providers.Dependency()
    kafka_consumer = providers.Dependency()
    topic_name = providers.Dependency()

    producer_client = providers.Singleton(
        ProducerClient,
        producer=kafka_producer,
        topic_name=topic_name
    )
    consumer_client = providers.Singleton(
        ConsumerClient,
        consumer=kafka_consumer
    )
    handler = providers.Factory(
        Handler,
        consumer_client=consumer_client,
        producer_client=producer_client,
    )


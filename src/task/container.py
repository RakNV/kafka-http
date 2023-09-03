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
    kafka_consumer_get = providers.Dependency()
    kafka_consumer_put = providers.Dependency()
    topic_name = providers.Dependency()

    producer_client = providers.Singleton(
        ProducerClient,
        producer=kafka_producer,
        topic_name=topic_name
    )
    consumer_client_get = providers.Factory(
        ConsumerClient,
        consumer=kafka_consumer_get
    )
    consumer_client_put = providers.Factory(
        ConsumerClient,
        consumer=kafka_consumer_put
    )
    handler = providers.Factory(
        Handler,
        consumer_client_get=consumer_client_get,
        consumer_client_put=consumer_client_put,
        producer_client=producer_client
    )

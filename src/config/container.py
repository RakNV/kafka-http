from dependency_injector import (
    containers,
    providers
)
from .config import (
    Service,
    Kafka
)


class Configuration(containers.DeclarativeContainer):
    kafka = providers.Configuration(pydantic_settings=[Kafka()])
    service = providers.Configuration(pydantic_settings=[Service()])

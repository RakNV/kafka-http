import random
from typing_extensions import (
    Any,
    Self
)
from src.task.container import TaskContainer
from src.task.models import (
    Task,
    TaskBase
)
from . import model_factories as factory
import pytest
from unittest import mock

class ConsumerMock:
    
    def __init__(self, sequence: list[Any]) -> None:
        self.sequence = sequence
        self.index = 0
        self.commit_call_count = 0

    def __iter__(self) -> Self:
        return self
    
    def commit(self) -> None:
        self.commit_call_count += 1

    def __next__(self) -> Any | None:
        if self.index >= len(self.sequence):
            raise StopIteration
        index = self.index
        self.index += 1
        return self.sequence[index]

class Message:

    def __init__(self, value):
        self.value = value


@pytest.fixture
def task_container() -> TaskContainer:
    return TaskContainer(
        kafka_producer=mock.Mock(),
        kafka_consumer=mock.Mock(),
        topic_name=mock.Mock()
    )

    
@pytest.fixture
def task_model() -> Task:
    return factory.TaskFactory.build()


@pytest.fixture
def task_base_model() -> TaskBase:
    return factory.TaskBaseFactory.build()


@pytest.fixture
def consumer_mock(
    task_base_model: TaskBase
) -> ConsumerMock:
    return ConsumerMock(
        sequence=[
            Message(
                value=task_base_model.dict()
            )
        ]
    )


@pytest.fixture
def random_seq() -> list[int]:
    return [random.randint(0, 10) for i in range(10)]


import pytest
from unittest import mock
from src.task.container import TaskContainer
from src.task.models import Task, TaskBase
from test.unit.task.conftest import ConsumerMock


def test_produce_task(
    task_container: TaskContainer,
    task_model: Task
) -> None:
    producer_mock = mock.Mock()
    task_container.kafka_producer.override(producer_mock)
    task_container.producer_client().produce_task(
        task=task_model
    ) 
    assert producer_mock.send.call_count == 1


def test_put_task(
    task_container: TaskContainer,
    consumer_mock: ConsumerMock,
    task_base_model: TaskBase
) -> None:
    task_container.kafka_consumer.override(consumer_mock)
    result = task_container.consumer_client().put_task()
    assert isinstance(result, Task)
    assert result.event_type == task_base_model.event_type
    assert result.meta == task_base_model.meta
    assert consumer_mock.commit_call_count == 1


def test_get_task(
    task_container: TaskContainer,
    random_seq: list[int]
) -> None:
    for i in range(len(random_seq)):
        res = task_container.consumer_client().get_task(queue_instance=random_seq)
        assert random_seq[0] == res


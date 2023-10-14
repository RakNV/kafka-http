from unittest import mock
from src.task.container import TaskContainer
from src.task.models import Task, TaskBase


def test_get_task(
    task_container: TaskContainer,
    task_model: Task
) -> None:
    consumer_mock = mock.Mock()
    consumer_mock.get_task.return_value = task_model
    task_container.consumer_client.override(consumer_mock)
    assert task_container.handler().get_task() == task_model
    assert consumer_mock.get_task.call_count == 1


def test_put_task(
    task_container: TaskContainer,
    task_model: Task
) -> None:
    consumer_mock = mock.Mock()
    consumer_mock.put_task.return_value = task_model
    task_container.consumer_client.override(consumer_mock)
    assert task_container.handler().put_task() == task_model
    assert consumer_mock.put_task.call_count == 1


def test_produce_task(
    task_container: TaskContainer,
    task_base_model: TaskBase
) -> None:
    producer_mock = mock.Mock()
    task_container.producer_client.override(producer_mock)
    assert task_container.handler().produce_task(
        task=task_base_model
    )
    assert producer_mock.produce_task.call_count == 1

from fastapi import HTTPException
from loguru import logger
from itertools import chain
from typing import Callable
from functools import wraps

from .models import Task


def remember(queue_instance: list):
    """
    It stores task in memory in given queue_instance
    """

    def wrapper(func: Callable):

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                task = None
                if kwargs.get("task"):
                    task = kwargs["task"]
                for arg in args:
                    if isinstance(arg, Task):
                        task = arg
                        break
                if not task:
                    raise ValueError
                queue_instance.append(task)
                return result
            except ValueError:
                logger.error("Task not found")
        return inner
    
    return wrapper


def sync(queue_instance: list):
    """
    Used to sync kafka and queue_instance
    """

    def wrapper(func: Callable):

        @wraps(func)
        def inner(*args, **kwargs):
            queue_instance.pop(0)
               
            return func(*args, **kwargs)
        return inner
    return wrapper
            

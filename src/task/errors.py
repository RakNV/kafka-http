from fastapi import HTTPException


QUEUE_IS_EMPTY_ERROR = HTTPException(
    status_code=404,
    detail={"message": "Task queue is empty", "code": 404}
)


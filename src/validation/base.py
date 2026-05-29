from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    status_code: int
    success: bool
    message: str
    data: T | None = None
    detail: Any | None = None

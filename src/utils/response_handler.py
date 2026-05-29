from typing import Any
from fastapi.responses import JSONResponse
from fastapi import status
from src.core.config import settings

class ApiResponse:
    @staticmethod
    def _payload(
            status_code: int,
            status_message: str,
            data: Any = None,
            detail: Any = None,
            success: bool = True,
    ) -> JSONResponse:
        safe_detail = detail if not settings.PRODUCTION else None

        return JSONResponse(
            status_code=status_code,
            content={
                "success": success,
                "status_message": status_message,
                "data": data,
                "detail": safe_detail
            }
        )

    @classmethod
    def success(cls, data: Any = None, status_message: str = "Success", status_code: int = status.HTTP_200_OK, detail: Any = None) -> JSONResponse:
        return cls._payload(status_code=status_code, status_message=status_message, data=data, detail=detail, success=True)

    @classmethod
    def failure(cls, status_code: int = status.HTTP_400_BAD_REQUEST, status_message: str = "Failure", detail: Any = None) -> JSONResponse:
        return cls._payload(status_code=status_code, status_message=status_message, detail=detail, success=False)
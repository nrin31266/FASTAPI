from fastapi import Request
from fastapi.responses import JSONResponse
from .base_exception import BaseException
from .base_error_code import BaseErrorCode


async def base_exception_handler(request: Request, exc: BaseException):
    """Handler cho BaseException"""
    return JSONResponse(
        status_code=exc.error_code.status.value,
        content={
            "code": exc.error_code.code,
            "message": exc.detail["message"] if isinstance(exc.detail, dict) else str(exc.detail),
        },
    )


async def global_exception_handler(request: Request, exc: Exception):
    """Handler cho các lỗi không xác định"""
    error = BaseErrorCode.INTERNAL_SERVER_ERROR
    return JSONResponse(
        status_code=error.status.value,
        content={"code": error.code, "message": str(exc)},
    )

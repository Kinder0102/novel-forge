
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "status_code": exc.status_code,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detail = "; ".join(
        f"{'.'.join(str(loc) for loc in e['loc'])}: {e['msg']}" for e in errors
    )
    return JSONResponse(
        status_code=422,
        content={
            "detail": detail,
            "error_code": "VALIDATION_ERROR",
            "status_code": 422,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("未處理的例外: %s %s", request.method, request.url.path)
    detail = getattr(exc, "message", str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "detail": detail,
            "error_code": "INTERNAL_ERROR",
            "status_code": 500,
        },
    )

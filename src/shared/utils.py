from typing import Callable, Optional, Any
from fastapi.requests import Request
from fastapi.responses import JSONResponse


def create_exception_handler(
    status_code: int, detail: Any = None
) -> Callable[[Request, Exception], JSONResponse]:
    def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=detail, status_code=status_code)

    return exception_handler

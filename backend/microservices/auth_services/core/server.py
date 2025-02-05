from typing import List

from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import router
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (AuthBackend, AuthenticationMiddleware,
                                      ResponseLoggerMiddleware,
                                      SQLAlchemyMiddleware)


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


"""
    TODO: Custom Exception
        This exception should be used to handle custom exceptions like
        `CustomException` and `BadRequestException` globally.
        The one made in the core/exceptions/base.py file.
"""


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


async def global_custom_exception(request: Request, exc: Exception):
    from icecream import ic

    ic(exc)
    try:
        if exc.code:
            return JSONResponse(
                status_code=exc.code,
                content={"error_code": exc.code, "message": str(exc)},
            )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error_code": 500, "message": str(exc)},
        )


def init_listeners(app_: FastAPI) -> None:
    app_.add_exception_handler(CustomException, custom_exception_handler)
    app_.add_exception_handler(Exception, global_custom_exception)


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(ResponseLoggerMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Auth Service",
        description="Authentication based service, for ecommerce platform",
        version="1.0.0",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()

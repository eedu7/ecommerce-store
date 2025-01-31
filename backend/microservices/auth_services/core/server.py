from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import router
from core.fastapi.middlewares import (AuthBackend, AuthenticationMiddleware,
                                      ResponseLoggerMiddleware,
                                      SQLAlchemyMiddleware)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
        Middleware(ResponseLoggerMiddleware),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Auth Service",
        description="The auth service of the e-commerce store",
        version="1.0.1",
        middleware=make_middleware(),
    )
    init_routers(app_)
    return app_


app = create_app()

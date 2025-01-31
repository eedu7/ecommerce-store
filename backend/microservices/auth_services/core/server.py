from fastapi import FastAPI

from api import router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Auth Service",
        description="The auth service of the e-commerce store",
        version="1.0.1",
    )
    init_routers(app_)
    return app_


app = create_app()

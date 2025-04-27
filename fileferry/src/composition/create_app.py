from fastapi import FastAPI

from composition.containers.application import ApplicationContainer
from shared.exceptions.middleware import ApplicationErrorMiddleware
from shared.logging.configuration import setup_logging
from shared.logging.middleware import RequestIdMiddleware
from transport.rest.routers.root import root_router


def create_app() -> FastAPI:
    """Создание и конфигурация FastAPI приложения."""
    setup_logging()

    container = ApplicationContainer()

    app = FastAPI()

    app.container = container  # type: ignore # если используешь интеграцию с FastAPI DI
    app.state.container = (
        container  # сохранить контейнер явно для доступа в любом месте приложения
    )

    container.wire(
        modules=[
            "composition.di",
        ],
    )

    # Подключение роутеров
    app.include_router(root_router)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(ApplicationErrorMiddleware)

    return app

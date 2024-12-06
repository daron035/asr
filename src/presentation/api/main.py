from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from vosk import Model

from src.infrastructure.containers import init_container
from src.presentation.api.config import APIConfig
from src.presentation.api.controllers.main import setup_controllers


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = init_container()
    model = container.resolve(Model)
    if not model:
        raise RuntimeError("Не удалось загрузить модель Vosk.")

    yield


def init_api(debug: bool = __debug__) -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        debug=debug,
        title="ASR Service",
        version="1.0.0",
    )
    setup_controllers(app)
    return app


async def run_api(app: FastAPI, api_config: APIConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        reload=True,
    )
    server = uvicorn.Server(config)
    await server.serve()

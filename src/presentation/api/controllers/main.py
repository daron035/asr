from fastapi import FastAPI

from .default import default_router
from .voice_rec import voice_rec_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(voice_rec_router)

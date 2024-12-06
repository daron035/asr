import os
import tomllib

from pathlib import Path
from typing import TypeVar

from adaptix import Retort

from src.presentation.api.config import Config


T = TypeVar("T")
DEFAULT_CONFIG_PATH = "./config/config.template.toml"
BASE_DIR = Path(__file__).parent.parent.resolve()
STATIC_DIR = Path(__file__).parent.parent.parent.resolve() / "static"


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_config(config_type: type[T], config_scope: str | None = None, path: str | None = None) -> T:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    data = read_toml(path)

    if config_scope is not None:
        data = data[config_scope]

    dcf = Retort()

    return dcf.load(data, config_type)


config = load_config(Config)

vosk_model = BASE_DIR / "application/asr/models" / config.api.vosk_model

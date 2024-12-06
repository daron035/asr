from dataclasses import dataclass, field


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = __debug__
    vosk_model: str = "vosk-model-ru-0.42"


@dataclass
class Config:
    api: APIConfig = field(default_factory=APIConfig)

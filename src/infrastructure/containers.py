from functools import lru_cache

from httpx import AsyncClient
from punq import Container, Scope
from vosk import Model

from src.application.asr.client import HttpClient
from src.application.asr.commands.recognize_file import RecognizeAudioFile, RecognizeAudioFileHandler
from src.application.asr.commands.recognize_url import RecognizeFromUrl, RecognizeFromUrlHandler
from src.application.asr.services.asr_service import AsrService, AsrServiceImpl
from src.infrastructure.config_loader import vosk_model
from src.infrastructure.mediator.mediator import MediatorImpl


@lru_cache(maxsize=1)
def init_container() -> Container:
    container = Container()
    container.register(Model, instance=Model(str(vosk_model)))
    container.register(AsrService, factory=lambda: _init_asr(container), scope=Scope.singleton)

    register_mediator(container)

    return container


def register_mediator(container: Container) -> None:
    container.register(MediatorImpl, factory=lambda: _init_mediator(container))


def _init_mediator(container: Container) -> MediatorImpl:
    mediator = MediatorImpl()

    recognize_url_handler = RecognizeFromUrlHandler(asr_service=container.resolve(AsrService))
    recognize_audio_file_handler = RecognizeAudioFileHandler(asr_service=container.resolve(AsrService))

    mediator.register_command_handler(RecognizeFromUrl, recognize_url_handler)
    mediator.register_command_handler(RecognizeAudioFile, recognize_audio_file_handler)

    return mediator


def _init_asr(container: Container) -> AsrServiceImpl:
    _model = container.resolve(Model)
    return AsrServiceImpl(client=HttpClient(AsyncClient()), model=_model)

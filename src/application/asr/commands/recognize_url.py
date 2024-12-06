from dataclasses import dataclass
from uuid import UUID

from src.application.asr.services.asr_service import AsrService
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler


@dataclass(frozen=True)
class RecognizeFromUrl(Command[UUID]):
    url: str


@dataclass(frozen=True)
class RecognizeFromUrlHandler(CommandHandler[RecognizeFromUrl, UUID]):
    asr_service: AsrService

    async def __call__(self, command: RecognizeFromUrl) -> UUID:
        response = await self.asr_service.process_url(command.url)
        return response

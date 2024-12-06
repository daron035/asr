from dataclasses import dataclass
from uuid import UUID

from fastapi import UploadFile

from src.application.asr.services.asr_service import AsrService
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler


@dataclass(frozen=True)
class RecognizeAudioFile(Command[UUID]):
    file: UploadFile


@dataclass(frozen=True)
class RecognizeAudioFileHandler(CommandHandler[RecognizeAudioFile, UUID]):
    asr_service: AsrService

    async def __call__(self, command: RecognizeAudioFile) -> UUID:
        file = command.file
        response = await self.asr_service.process_file(file)

        return response

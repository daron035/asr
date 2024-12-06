from fastapi import APIRouter, Depends, UploadFile
from punq import Container

from src.application.asr.commands.recognize_file import RecognizeAudioFile
from src.application.asr.commands.recognize_url import RecognizeFromUrl
from src.infrastructure.containers import init_container
from src.infrastructure.mediator.mediator import MediatorImpl


voice_rec_router = APIRouter(
    prefix="/api",
    tags=["voice"],
)


@voice_rec_router.post(
    "/recognition_from_url",
    description="Example url - https://www.russianforfree.com/resources/audio_dialogues/01-01-lutshiy-drug.mp3",
)
async def recognize_file_from_url(
    data: RecognizeFromUrl,
    container: Container = Depends(init_container),
):
    mediator: MediatorImpl = container.resolve(MediatorImpl)
    response = await mediator.send(data)
    return response


@voice_rec_router.post("/asr")
async def recognize_audio_file(
    file: UploadFile,
    container: Container = Depends(init_container),
):
    mediator: MediatorImpl = container.resolve(MediatorImpl)
    response = await mediator.send(RecognizeAudioFile(file))
    return response

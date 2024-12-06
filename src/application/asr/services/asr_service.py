import asyncio
import json
import os
import wave

from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

import aiofiles

from fastapi import UploadFile
from pydub import AudioSegment
from vosk import KaldiRecognizer, Model

from src.application.asr.client import HttpClient


class AsrService(Protocol):
    @abstractmethod
    async def process_url(self, url: str):
        raise NotImplementedError

    @abstractmethod
    async def process_file(self, file: UploadFile):
        raise NotImplementedError


@dataclass
class AsrServiceImpl:
    client: HttpClient
    model: Model

    async def analyze_transcription(self, result: list) -> dict:
        dialog = []
        result_duration = {"receiver": 0, "transmitter": 0}
        current_source = "receiver"

        for segment in result:
            text = segment.get("text", "")
            duration = len(text.split())
            raised_voice = "!" in text or text.isupper()
            gender = "male" if current_source == "receiver" else "female"

            dialog.append(
                {
                    "source": current_source,
                    "text": text,
                    "duration": duration,
                    "raised_voice": raised_voice,
                    "gender": gender,
                },
            )

            result_duration[current_source] += duration
            current_source = "transmitter" if current_source == "receiver" else "receiver"

        return {"dialog": dialog, "result_duration": result_duration}

    async def convert_audio_to_wav(self, input_file_path: str, output_file_path: str) -> None:
        audio = AudioSegment.from_file(input_file_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(output_file_path, format="wav")

    async def process_audio(self, file_path: str) -> list:
        def _process_audio_sync():
            with wave.open(file_path, "rb") as wf:
                if wf.getnchannels() != 1 or wf.getframerate() not in (16000, 8000):
                    raise ValueError("Аудиофайл должен быть монофоническим WAV с частотой 16kHz.")

                recognizer = KaldiRecognizer(self.model, wf.getframerate())
                recognizer.SetWords(True)

                results = []
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        results.append(json.loads(recognizer.Result()))

                results.append(json.loads(recognizer.FinalResult()))
                return results

        return await asyncio.to_thread(_process_audio_sync)

    async def process_url(self, url: str) -> dict:
        temp_mp3_path = await self.client.get_audio(url)
        temp_wav_path = f"{temp_mp3_path}.wav"

        try:
            # Конвертируем в WAV
            await self.convert_audio_to_wav(temp_mp3_path, temp_wav_path)

            # Обрабатываем WAV файл
            transcription = await self.process_audio(temp_wav_path)

            # Анализируем результаты
            response = await self.analyze_transcription(transcription)
        finally:
            os.remove(temp_mp3_path)
            os.remove(temp_wav_path)

        return response

    async def process_file(self, file: UploadFile):
        temp_mp3_path = f"/tmp/{file.filename}"
        temp_wav_path = f"/tmp/{file.filename}.wav"

        # Сохраняем загруженный файл
        async with aiofiles.open(temp_mp3_path, "wb") as f:
            await f.write(await file.read())

        try:
            # Конвертируем в WAV
            await self.convert_audio_to_wav(temp_mp3_path, temp_wav_path)

            # Обрабатываем WAV файл
            transcription = await self.process_audio(temp_wav_path)

            # Анализируем результаты
            response = await self.analyze_transcription(transcription)
        finally:
            os.remove(temp_mp3_path)
            os.remove(temp_wav_path)

        return response

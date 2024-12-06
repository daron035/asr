from dataclasses import dataclass
from uuid import uuid4

import aiofiles

from httpx import AsyncClient


@dataclass
class HttpClient:
    http_client: AsyncClient

    async def get_audio(self, url: str):
        tmp_path = f"/tmp/{uuid4()}"
        async with self.http_client.stream("GET", url) as response:
            async with aiofiles.open(tmp_path, "wb") as download_file:
                async for chunk in response.aiter_bytes():
                    await download_file.write(chunk)

        return tmp_path

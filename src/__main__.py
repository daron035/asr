import asyncio

import uvicorn

from src.infrastructure.config_loader import config
from src.presentation.api.__main__ import main


if __name__ == "__main__":
    if config.api.debug:
        print(config.api)  # noqa
        uvicorn.run("src.presentation.api.main:init_api", reload=True, factory=True)
    else:
        asyncio.run(main())

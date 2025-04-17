import asyncio
import os
from pathlib import Path

from pyrogram import Client

from app.config import load_environment

TIMEOUT = 3


async def create_session(config_path: str) -> None:
    load_environment(config_path)

    app = Client(
        name=os.environ["BOT_NAME"],
        api_id=int(os.environ["API_ID"]),
        api_hash=os.environ["API_HASH"],
    )

    async with app:
        await asyncio.gather(
            # app.start(),
            asyncio.sleep(TIMEOUT)
        )
        await app.stop()


def check_session() -> bool:
    project_root = Path(__file__).parent.parent.resolve()
    return any(
        file.suffix == ".session" and file.is_file()
        for file in project_root.iterdir()
    )

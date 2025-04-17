import asyncio
from logging import Logger
from typing import TYPE_CHECKING

from pyrogram import ContinuePropagation
from pyrogram.errors import FloodWait, RPCError
from pyrogram.handlers.handler import Handler
from pyrogram.types import Message

if TYPE_CHECKING:
    from app.base import Kostritsky


class ErrorHandlerMiddleware(Handler):
    def __init__(self, logger: Logger):
        self.logger = logger

    async def __call__(
        self, client: "Kostritsky", message: Message, next_handler: Handler
    ):
        try:
            return await next_handler(client, message)
        except FloodWait as e:
            self.logger.warning("Flood wait: Sleeping for %s seconds", e.value)
            await asyncio.sleep(e.value)
            return await self(client, message, next_handler)
        except RPCError as e:
            self.logger.error("Telegram error [%s]: %r", e.ID, e)
        except Exception:
            self.logger.exception("Critical error in handler!\n")

        return ContinuePropagation()


def setup_middlewares(app: "Kostritsky"):
    logger = app.logger
    error_handler = ErrorHandlerMiddleware(logger)
    app.add_handler(error_handler, group=-1)

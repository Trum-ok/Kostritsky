import logging
import sys
from logging import Logger
from typing import TYPE_CHECKING

from pyrogram import ContinuePropagation, filters
from pyrogram.handlers.handler import Handler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message

if TYPE_CHECKING:
    from app.base import Kostritsky

BOT_LOGGER = "bot"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-25s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        # RotatingFileHandler(  # TODO: расскоментировать перед релизом (мб)
        #     "bot.log",
        #     maxBytes=5*1024*1024,
        #     backupCount=3
        # )
    ],
)


class LoggingMiddleware(MessageHandler):  # TODO: отражать в логах удаление и тд
    def __init__(self, logger: Logger):
        super().__init__(self._log_message, filters.all)
        self.logger = logger

    async def __call__(
        self, client: "Kostritsky", message: Message, next_handler: Handler
    ):
        self._log_message(message)
        try:
            return await next_handler(client, message)
        finally:
            pass

    async def _log_message(self, client: "Kostritsky", message: Message):
        log_data = {
            "chat_id": message.chat.id,
            "user_id": message.from_user.id if message.from_user else "N/A",
            "message_id": message.id,
            "content": message.text or message.caption or "<media>",
            # "is_edited": message.edited,
            "is_service": message.service is not None,
        }

        self.logger.info(
            "New message [%s] in chat %s: %s",
            message.id,
            message.chat.id,
            log_data["content"][:50] + "..."
            if len(log_data["content"]) > 50
            else log_data["content"],
        )

        if message.media:
            self.logger.debug(
                "Media details: %s (type: %s)",
                message.media,
                message.media.value if message.media else "unknown",
            )

        return ContinuePropagation()


def setup_logging(app: "Kostritsky") -> None:
    main_logger = logging.getLogger(BOT_LOGGER)
    main_logger.setLevel(logging.INFO)

    standard_formatter = logging.Formatter(
        "%(asctime)s | %(name)s - %(levelname)s - %(message)s",
    )
    error_formatter = logging.Formatter(
        "%(asctime)s | %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",  # noqa: E501
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(standard_formatter)
    console_handler.setLevel(logging.INFO)

    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setFormatter(error_formatter)
    error_handler.setLevel(logging.WARNING)

    app.logger = main_logger
    logging_middleware = LoggingMiddleware(main_logger)
    app.add_handler(logging_middleware, group=-100)

import os
from logging import Logger, getLogger

from pyrogram import Client

from app.config import Config, setup_config
from app.logger import BOT_LOGGER

__all__ = ("Kostritsky",)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../.env")


class Kostritsky(Client):
    def __init__(self, *args, **kwargs):
        self._config: Config | None = None
        self._logger: Logger | None = None
        super().__init__(
            name=self.config.bot_name,
            api_id=self.config.api_id,
            api_hash=self.config.api_hash,
        )

    @property
    def config(self):
        if self._config is None:
            self._config = setup_config(CONFIG_PATH)
        return self._config.tg

    @property
    def logger(self) -> Logger:
        if self._logger is None:
            self._logger = getLogger(BOT_LOGGER)
        return self._logger

    @logger.setter
    def logger(self, value: Logger) -> None:
        if not isinstance(value, Logger):
            raise TypeError("Expected logging.Logger instance.")
        self._logger = value

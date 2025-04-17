import os
from dataclasses import dataclass

from dotenv import load_dotenv


def load_environment(config_path: str | None = None) -> None:
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), ".env"
        )
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    load_dotenv(config_path, override=True)


load_environment()
FROM_GROUP = int(os.environ["FROM_GROUP"])
TO_CHANNEL = int(os.environ["TO_CHANNEL"])


@dataclass
class TelegramConfig:
    bot_name: str
    api_id: int
    api_hash: str


@dataclass
class Config:
    tg: TelegramConfig | None = None


def setup_config(config_path: str):
    load_environment(config_path)

    tg_config = TelegramConfig(
        bot_name=os.environ["BOT_NAME"],
        api_id=int(os.environ["API_ID"]),
        api_hash=os.environ["API_HASH"],
    )

    return Config(tg=tg_config)

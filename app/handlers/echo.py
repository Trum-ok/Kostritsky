from typing import TYPE_CHECKING, Any

from pyrogram import filters
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message

if TYPE_CHECKING:
    from app.bot import Kostritsky


class EchoHandler(MessageHandler):
    def __init__(self):
        super().__init__(self.handle_message, filters.chat("me"))
        self.echo_enabled = True

    async def check(self, client: "Kostritsky", message: Message) -> bool:
        if not self.echo_enabled:
            return False

        return await super().check(client, message)

    async def handle_message(
        self, client: "Kostritsky", message: Message, *args: Any
    ) -> None:
        await client.send_message("me", message.text)


echo_handler = EchoHandler()

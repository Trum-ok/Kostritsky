from collections import defaultdict
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from pyrogram import filters
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message

from app.config import FROM_GROUP, TO_CHANNEL

if TYPE_CHECKING:
    from app.bot import Kostritsky


class KostritskyHandler(MessageHandler):
    def __init__(self):
        self.handlers = defaultdict(list[tuple[filters.Filter, Callable]])
        super().__init__(self._route_messages, filters.chat(FROM_GROUP))

    def add_handler(self, flt: filters.Filter, group: int | None = 0):
        def decorator(func: Callable):
            self.handlers[group].append((flt, func))
            return func

        return decorator

    async def _route_messages(
        self, client: "Kostritsky", message: Message, *args: Any
    ) -> None:
        for group in sorted(self.handlers.keys()):
            for flt, handler in self.handlers[group]:
                if await flt(client, message):
                    await handler(client, message, *args)
                    return


kostritsky_handler = KostritskyHandler()


@kostritsky_handler.add_handler(~filters.service | filters.sticker)
async def forward_to_channel(client: "Kostritsky", message: Message):
    await client.forward_messages("me", FROM_GROUP, message.id)  # TODO: me


# @kostritsky_handler.add_handler(filters.group & filters.ed)
# async def track_edits(client: Kostritsky, message: Message):
#     pass

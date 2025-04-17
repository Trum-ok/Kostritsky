from typing import TYPE_CHECKING

from .echo import echo_handler
from .kostritsky import kostritsky_handler

if TYPE_CHECKING:
    from app.bot import Kostritsky

handlers = [
    kostritsky_handler,
    echo_handler,
]


def setup_handlers(client: "Kostritsky"):  # TODO: пофиксить приоритет
    for id_, handler in enumerate(handlers):
        client.add_handler(handler, group=id_)

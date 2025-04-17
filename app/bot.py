from app.base import Kostritsky
from app.handlers import setup_handlers
from app.logger import setup_logging
from app.middleware import setup_middlewares

leksandure = Kostritsky()


def setup_leksandure() -> Kostritsky:
    setup_logging(leksandure)
    leksandure.logger.info("Logging was set up")
    setup_middlewares(leksandure)
    leksandure.logger.info("Middlewares were set up")
    setup_handlers(leksandure)
    leksandure.logger.info("Handlers were set up")

    leksandure.logger.info("Делишос")
    return leksandure

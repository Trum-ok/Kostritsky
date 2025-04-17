import asyncio
import logging
import os

from app.bot import setup_leksandure
from app.session import check_session, create_session

logger = logging.getLogger(__name__)


def main(config_path: str):
    logger.info('printf("Jopa\\n")')
    if not check_session():
        asyncio.run(create_session(config_path))
        logger.info(".session is ready.\n\n\n")

    san = setup_leksandure()
    san.run()


if __name__ == "__main__":
    main(config_path=os.path.join(os.path.dirname(__file__), ".env"))

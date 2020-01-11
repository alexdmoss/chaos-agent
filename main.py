import sys
import logging
from os import getenv

logging.basicConfig(level=logging.INFO, format="-> [%(levelname)s] [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M")

logger = logging.getLogger(__name__)


if getenv("DEBUG"):
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    logger.debug("Debugging is ENABLED")


def main():
    logger.info("BEHOLD THE AGENT OF CHAOS")


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()

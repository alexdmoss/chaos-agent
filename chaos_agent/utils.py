import logging
from os import getenv
from random import seed, randint


def configure_logging():
    logging.basicConfig(level=logging.INFO, format="-> [%(levelname)s] [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M")
    if getenv("DEBUG") == "True":
        logging.getLogger(__name__).setLevel(logging.DEBUG)
    return logging.getLogger(__name__)


def get_random_int(limit):
    seed()
    return randint(0, (limit - 1))

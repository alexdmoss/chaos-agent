import logging
import yaml
import time
from os import getenv
from random import seed, randint
from dataclasses import dataclass, field
from dacite import from_dict, exceptions
from typing import List


def configure_logging():
    logging.basicConfig(level=logging.INFO, format="-> [%(levelname)s] [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M")
    if getenv("DEBUG") == "True":
        logging.getLogger(__name__).setLevel(logging.DEBUG)
    return logging.getLogger(__name__)


logger = configure_logging()


def get_random_int(limit):
    seed()
    return randint(0, (limit - 1))


def load_config(filename):
    data = {}
    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
    except IOError as e:
        logger.error(f"Could not open config yaml, error was: {e}")
        logger.warning(f"Default config values will be used: {Config()}")
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse config yaml, error was: {e}")
        logger.warning(f"Default config values will be used: {Config()}")

    if data:
        try:
            return from_dict(data_class=Config, data=data)
        except exceptions.WrongTypeError as e:
            logger.error(f"Bad data type in config file. See error message: {e}")
            logger.warning(f"Default config values will be used: {Config()}")
            return Config()
        except TypeError as e:
            logger.error(f"Bad data type in config file. See error message: {e}")
            logger.warning(f"Default config values will be used: {Config()}")
            return Config()
    else:
        return Config()


def calc_interval(frequency, randomise=False):
    if randomise:
        interval = get_random_int(limit=frequency)
        if interval == 0:
            interval = frequency
    else:
        interval = frequency
    return interval


def set_default_ns_exclusions():
    return ['kube-system']


@dataclass
class Config:
    dryRun: bool = True
    debug: bool = False
    updateFrequency: int = 60
    randomiseFrequency: bool = False
    numPodsToDelete: int = 1
    numNodesToDelete: int = 0
    excludedNamespaces: List = field(default_factory=set_default_ns_exclusions)

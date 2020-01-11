import sys
import logging
from os import getenv

from chaos_agent.utils import load_k8s_context, list_all_pods

logging.basicConfig(level=logging.INFO, format="-> [%(levelname)s] [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M")

logger = logging.getLogger(__name__)


def main():
    logger.info("BEHOLD THE AGENT OF CHAOS")

    if getenv("DEBUG") == "True":
        logging.getLogger(__name__).setLevel(logging.DEBUG)
        logger.debug("Debugging is ENABLED")

    load_k8s_context()

    pods = list_all_pods()

    logger.debug(pods)


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()

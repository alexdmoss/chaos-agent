import sys

from chaos_agent.client import load_k8s_context
from chaos_agent.pods import find_and_terminate_pods
# from chaos_agent.nodes import find_and_terminate_nodes
from chaos_agent.utils import configure_logging


logger = configure_logging()


def main():

    logger.info("BEHOLD THE AGENT OF CHAOS")
    logger.debug("Debugging is ENABLED")

    load_k8s_context()

    find_and_terminate_pods()

    # find_and_terminate_nodes()


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()

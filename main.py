import sys
import time

from chaos_agent.client import load_k8s_context
from chaos_agent.pods import find_and_terminate_pods
# from chaos_agent.nodes import find_and_terminate_nodes
from chaos_agent.utils import configure_logging, load_config


logger = configure_logging()


def main():

    logger.info("BEHOLD, the:")
    with open(r"ascii.txt") as a:
        logger.info(f"{a.read()}")

    config = load_config("config.yaml")

    logger.debug("Config initalised with the following values:")
    logger.debug(f"  Debug:                  {config.debug}")
    logger.debug(f"  Dry Run:                {config.dryRun}")
    logger.debug(f"  Update Frequency:       {config.updateFrequency}")
    logger.debug(f"  Randomised Frequency:   {config.randomiseFrequency}")
    logger.debug(f"  Pods To Delete:         {config.numPodsToDelete}")
    logger.debug(f"  Nodes To Delete:        {config.numNodesToDelete}")
    logger.debug(f"  ExcludedNamespaces:     {config.excludedNamespaces}")

    load_k8s_context()

    while True:
        find_and_terminate_pods()
        # find_and_terminate_nodes()
        time.sleep(config.updateFrequency)


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()

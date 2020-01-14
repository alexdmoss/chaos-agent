import sys
import time
from os import getenv

from chaos_agent.client import load_k8s_context
from chaos_agent.pods import find_and_terminate_pods
# from chaos_agent.nodes import find_and_terminate_nodes
from chaos_agent.utils import configure_logging, load_config, calc_interval


logger = configure_logging()


def main():

    logger.info('BEHOLD, the:')
    with open(r'ascii.txt') as a:
        logger.info(f'{a.read()}')

    logger.debug('DEBUG mode enabled - actions will be printed to log')

    cfg_file = getenv('CFG_FILE', 'config.yaml')
    config = load_config(cfg_file)

    logger.debug('Config initalised with the following values:')
    logger.debug(f'  Dry Run:                {config.dryRun}')
    logger.debug(f'  Grace Period:           {config.gracePeriod}')
    logger.debug(f'  Update Frequency:       {config.updateFrequency}')
    logger.debug(f'  Randomised Frequency:   {config.randomiseFrequency}')
    logger.debug(f'  Pods To Delete:         {config.numPodsToDelete}')
    logger.debug(f'  Nodes To Delete:        {config.numNodesToDelete}')
    logger.debug(f'  ExcludedNamespaces:     {config.excludedNamespaces}')

    load_k8s_context()

    while True:
        find_and_terminate_pods(config.numPodsToDelete, config.dryRun, config.gracePeriod)
        # find_and_terminate_nodes()
        interval = calc_interval(frequency=config.updateFrequency, randomise=config.randomiseFrequency)
        logger.debug(f'Sleeping for {interval}')
        time.sleep(interval)


def init():
    if __name__ == '__main__':
        sys.exit(main())


init()

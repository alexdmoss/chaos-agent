from kubernetes import client
from kubernetes.client.rest import ApiException

from chaos_agent.utils import get_random_int
from chaos_agent.utils import configure_logging


logger = configure_logging()


def find_and_terminate_nodes(dry_run):
    nodes = list_nodes()
    if nodes:
        node = select_random_node(nodes)
        # delete_node(node=node, dry_run=dry_run)
        logger.info(f"would delete {node} here")


def list_nodes():
    core_api = client.CoreV1Api()
    try:
        nodes = [node.metadata.name for node in core_api.list_node(timeout_seconds=60).items]
        logger.debug(f"Found {len(nodes)} nodes")
    except ApiException as e:
        nodes = []
        logger.error(f"Could not fetch list of all nodes, error message: {e}")
    return nodes


def select_random_node(nodes):
    node = get_random_int(len(nodes))
    return nodes[node]


def delete_node(node, dry_run=False, grace=0):
    if dry_run:
        logger.info(f"DRY-RUN: Node {node} would have been deleted")
    else:
        core_api = client.CoreV1Api()
        try:
            logger.debug(f"Deleting node: {node}")
            core_api.delete_node(node, grace_period_seconds=grace)
        except ApiException as e:
            logger.error(f"Failed to delete node, error message: {e}")

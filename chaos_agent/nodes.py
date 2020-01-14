from kubernetes import client
from kubernetes.client.rest import ApiException

from chaos_agent.utils import get_random_list_of_ints
from chaos_agent.utils import configure_logging


logger = configure_logging()


def find_and_terminate_nodes(num_nodes=1, dry_run=True, grace=0):
    nodes = list_nodes()
    if nodes:
        return [delete_node(node=node, dry_run=dry_run, grace=grace) for node in select_random_nodes(nodes, num_nodes)]


def list_nodes():
    core_api = client.CoreV1Api()
    try:
        nodes = [node.metadata.name for node in core_api.list_node(timeout_seconds=60).items]
        logger.debug(f"Found {len(nodes)} nodes")
        return nodes
    except ApiException as e:
        logger.error(f"Could not fetch list of all nodes, error message: {e}")
        return None


def select_random_nodes(nodes, num_nodes=1):
    if len(nodes) < num_nodes:
        num_nodes = len(nodes)
        logger.warning("Found fewer nodes than the number to be terminated! All nodes will be deleted")
    return [nodes[i] for i in get_random_list_of_ints(len(nodes), num_nodes)]


def delete_node(node, dry_run=False, grace=0):
    if dry_run:
        logger.info(f"DRY-RUN: Node {node} would have been deleted")
    else:
        core_api = client.CoreV1Api()
        try:
            core_api.delete_node(name=node, grace_period_seconds=grace)
            logger.debug(f"Deleted node: {node}")
        except ApiException as e:
            logger.error(f"Failed to delete node, error message: {e}")

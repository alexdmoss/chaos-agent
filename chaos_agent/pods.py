from kubernetes import client
from kubernetes.client.rest import ApiException

from chaos_agent.utils import get_random_int, get_random_list_of_ints
from chaos_agent.utils import configure_logging


logger = configure_logging()


def find_and_terminate_pods(num_pods=1, dry_run=True):
    pods = list_pods()
    if pods:
        return [delete_pod(pod, dry_run=dry_run) for pod in select_random_pods(pods, num_pods)]


def list_all_pods():
    core_api = client.CoreV1Api()
    try:
        return core_api.list_pod_for_all_namespaces(timeout_seconds=60)
    except ApiException as e:
        logger.error(f"Could not fetch list of pods, error message: {e}")
        return None


def list_pods():
    all_pods = list_all_pods()
    if all_pods:
        pods = [[pod.metadata.name, pod.metadata.namespace] for pod in all_pods.items]
        logger.debug(f"Found {len(pods)} pods")
        return pods


def select_random_pods(pods, num_pods=1):
    if len(pods) < num_pods:
        num_pods = len(pods)
        logger.warning("Found fewer pods than the number to be terminated! All pods will be deleted per cycle")
    pod_nums = get_random_list_of_ints(len(pods), num_pods)
    return [tuple(pods[i]) for i in pod_nums]


def delete_pod(pod, dry_run=False, grace=0):
    name = pod[0]
    ns = pod[1]
    if dry_run:
        logger.info(f"DRY-RUN: Pod {name} in {ns} would have been deleted")
    else:
        core_api = client.CoreV1Api()
        try:
            core_api.delete_namespaced_pod(name=name, namespace=ns, grace_period_seconds=grace)
            logger.debug(f"Deleted pod: {name} in {ns}")
        except ApiException as e:
            logger.error(f"Failed to delete pod, error message: {e}")
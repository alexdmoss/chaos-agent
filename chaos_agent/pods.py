from kubernetes import client
from kubernetes.client.rest import ApiException

from chaos_agent.utils import get_random_int
from chaos_agent.utils import configure_logging


logger = configure_logging()


def find_and_terminate_pods(dry_run):
    pods = list_pods()
    if pods:
        pod_name, pod_ns = select_random_pod(pods)
        delete_pod(name=pod_name, ns=pod_ns, dry_run=dry_run)


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


def select_random_pod(pods):
    pod = pods[get_random_int(len(pods))]
    return pod[0], pod[1]


def delete_pod(name, ns, dry_run=False, grace=0):
    if dry_run:
        logger.info(f"DRY-RUN: Pod {name} in {ns} would have been deleted")
    else:
        core_api = client.CoreV1Api()
        try:
            core_api.delete_namespaced_pod(name=name, namespace=ns, grace_period_seconds=grace)
            logger.debug(f"Deleted pod: {name} in {ns}")
        except ApiException as e:
            logger.error(f"Failed to delete pod, error message: {e}")

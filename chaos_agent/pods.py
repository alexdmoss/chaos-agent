from kubernetes import client
from kubernetes.client.rest import ApiException

from chaos_agent.utils import get_random_list_of_ints
from chaos_agent.utils import configure_logging


logger = configure_logging()


def find_and_terminate_pods(num_pods=1, dry_run=True, grace=0, inclusions=[], exclusions=[]):
    pods = list_pods(included_namespacees=inclusions, excluded_namespaces=exclusions)
    if pods:
        return [delete_pod(pod=pod, dry_run=dry_run, grace=grace) for pod in select_random_pods(pods, num_pods)]


def list_all_pods():
    core_api = client.CoreV1Api()
    try:
        return core_api.list_pod_for_all_namespaces(timeout_seconds=60)
    except ApiException as e:
        logger.error(f"Could not fetch list of pods, error message: {e}")
        return None


def list_pods(included_namespaces=[], excluded_namespaces=[]):
    all_pods = list_all_pods()
    if all_pods:
        if len(included_namespaces) > 0:
            pods = [[pod.metadata.name, pod.metadata.namespace]
                    for pod in all_pods.items if pod.metadata.namespace in included_namespaces]
        else:
            pods = [[pod.metadata.name, pod.metadata.namespace]
                    for pod in all_pods.items if pod.metadata.namespace not in excluded_namespaces]
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

import logging

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.rest import ApiException


logging.basicConfig(level=logging.INFO, format="-> [%(levelname)s] [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M")

logger = logging.getLogger(__name__)


def load_k8s_context():
    try:
        config.load_incluster_config()  # on cluster
    except ConfigException:
        config.load_kube_config()  # local


def list_all_pods():

    core_api = client.CoreV1Api()
    try:
        pods = [[pod.metadata.name, pod.metadata.namespace]
                for pod in core_api.list_pod_for_all_namespaces(timeout_seconds=60).items]
    except ApiException as e:
        logger.error(f"Could not fetch list of all pods: {e}")

    logger.debug(f"{pods}")
    logger.debug(f"Found {len(pods)} pods")
    return pods

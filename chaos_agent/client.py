from kubernetes import config
from kubernetes.config.config_exception import ConfigException


def load_k8s_context():
    try:
        config.load_incluster_config()  # on cluster
    except ConfigException:
        config.load_kube_config()  # local

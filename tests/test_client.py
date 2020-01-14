import chaos_agent.client as client
from kubernetes.config.config_exception import ConfigException


def test_load_context(mocker):
    # This effectively mocks out the whole context getting/setting for coverage :/
    mocker.patch('chaos_agent.client.config.load_kube_config')
    stub_in_cluster = mocker.patch('chaos_agent.client.config.load_incluster_config')

    client.load_k8s_context()

    stub_in_cluster.side_effect = ConfigException('doesnotmatter')
    client.load_k8s_context()

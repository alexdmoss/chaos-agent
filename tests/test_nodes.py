import chaos_agent.nodes

import json
from types import SimpleNamespace as Namespace
from kubernetes.client.rest import ApiException


def test_find_and_terminate_nodes_stubbed(mocker, monkeypatch, caplog):
    monkeypatch.setenv('DEBUG', 'True')
    chaos_agent.utils.configure_logging()
    mocker.patch('chaos_agent.nodes.list_nodes')
    mocker.patch('chaos_agent.nodes.select_random_nodes', return_value=['gke-mw-prod-np-0-3be8d635-rwd1'])
    mocker.patch('chaos_agent.nodes.client.CoreV1Api.delete_node')
    chaos_agent.nodes.find_and_terminate_nodes(num_nodes=1, dry_run=False)
    assert 'Deleted node:' in caplog.text


def test_find_and_terminate_nodes_dry_run(mocker, caplog):
    mocker.patch('chaos_agent.nodes.list_nodes')
    mocker.patch('chaos_agent.nodes.select_random_nodes', return_value=['gke-mw-prod-np-0-3be8d635-rwd1'])
    chaos_agent.nodes.find_and_terminate_nodes(num_nodes=1, dry_run=True)
    assert 'DRY-RUN:' in caplog.text
    assert 'would have been deleted' in caplog.text


def test_find_no_nodes(mocker):
    mocker.patch('chaos_agent.nodes.list_nodes', return_value=None)
    chaos_agent.nodes.find_and_terminate_nodes(dry_run=False)


def test_list_nodes(mocker):
    with open('./tests/mocks/node-list.json', 'r') as f:
        raw_data = f.read()
        node_list = json.loads(raw_data, object_hook=lambda d: Namespace(**d))
    mocker.patch('chaos_agent.nodes.client.CoreV1Api.list_node', return_value=node_list)

    nodes = chaos_agent.nodes.list_nodes()

    expected_node = 'gke-mw-prod-np-0-947e5a45-vpdd'
    assert any([node for node in nodes if node == expected_node])


def test_list_nodes_is_zero(mocker):
    mocker.patch('chaos_agent.nodes.list_nodes', return_value=None)
    nodes = chaos_agent.nodes.list_nodes()
    assert nodes is None


def test_list_nodes_fails(mocker):
    mocker.patch('chaos_agent.nodes.client.CoreV1Api.list_node', side_effect=ApiException('wibble'))
    nodes = chaos_agent.nodes.list_nodes()
    assert nodes is None


def test_select_one_random_node(mocker):
    mock_nodes = ['node-1', 'node-2', 'node-3', 'node-4', 'node-5', 'node-6', 'node-7']

    stub_random_ints = mocker.patch('chaos_agent.nodes.get_random_list_of_ints')

    stub_random_ints.return_value = [0]
    node = chaos_agent.nodes.select_random_nodes(mock_nodes)
    assert len(node) == 1
    assert node == ['node-1']

    stub_random_ints.return_value = [6]
    node = chaos_agent.nodes.select_random_nodes(nodes=mock_nodes)
    assert len(node) == 1
    assert node == ['node-7']


def test_select_three_random_nodes(mocker):
    mock_nodes = ['node-1', 'node-2', 'node-3', 'node-4', 'node-5', 'node-6', 'node-7']

    stub_random_ints = mocker.patch('chaos_agent.nodes.get_random_list_of_ints')

    stub_random_ints.return_value = [1, 3, 5]
    node = chaos_agent.nodes.select_random_nodes(nodes=mock_nodes, num_nodes=3)
    assert len(node) == 3
    assert node[0] == 'node-2'
    assert node[1] == 'node-4'
    assert node[2] == 'node-6'


def test_select_more_nodes_than_available(mocker):
    mock_nodes = ['node-1', 'node-2', 'node-3']

    node = chaos_agent.nodes.select_random_nodes(nodes=mock_nodes, num_nodes=5)
    assert len(node) == 3
    assert node[0] == 'node-1'
    assert node[1] == 'node-2'
    assert node[2] == 'node-3'


def test_delete_node(mocker, caplog, monkeypatch):
    monkeypatch.setenv('DEBUG', 'True')
    chaos_agent.utils.configure_logging()
    mocker.patch('chaos_agent.nodes.client.CoreV1Api.delete_node')
    chaos_agent.nodes.delete_node(node='node-1')
    assert 'Deleted node: node-1' in caplog.text


def test_failed_delete_node(mocker, caplog, monkeypatch):
    monkeypatch.setenv('DEBUG', 'True')
    chaos_agent.utils.configure_logging()
    stub_delete_node = mocker.patch('chaos_agent.nodes.client.CoreV1Api.delete_node')
    stub_delete_node.side_effect = ApiException('wobble')
    chaos_agent.nodes.delete_node(node='node-1')
    assert 'Failed to delete node, error message: (wobble)' in caplog.text

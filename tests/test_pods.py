import chaos_agent.pods

import json
from types import SimpleNamespace as Namespace
from kubernetes.client.rest import ApiException


def test_find_and_terminate_pods_stubbed(mocker, monkeypatch, caplog):
    monkeypatch.setenv('DEBUG', 'True')
    chaos_agent.utils.configure_logging()
    mocker.patch('chaos_agent.pods.list_pods')
    mocker.patch('chaos_agent.pods.select_random_pods', return_value=['cert-manager-5c5f4b9b49-m6xd8', 'cert-manager'])
    mocker.patch('chaos_agent.pods.client.CoreV1Api.delete_namespaced_pod')
    chaos_agent.pods.find_and_terminate_pods(dry_run=False)
    assert 'Deleted pod:' in caplog.text


def test_find_and_terminate_pods_dry_run(mocker, caplog):
    mocker.patch('chaos_agent.pods.list_pods')
    mocker.patch('chaos_agent.pods.select_random_pods', return_value=['cert-manager-5c5f4b9b49-m6xd8', 'cert-manager'])
    chaos_agent.pods.find_and_terminate_pods(dry_run=True)
    assert 'DRY-RUN:' in caplog.text
    assert 'would have been deleted' in caplog.text


def test_find_no_pods(mocker):
    mocker.patch('chaos_agent.pods.list_pods', return_value=None)
    chaos_agent.pods.find_and_terminate_pods(dry_run=False)


def test_list_pods(mocker):
    with open('./tests/mocks/pod-list.json', 'r') as f:
        raw_data = f.read()
        pod_list = json.loads(raw_data, object_hook=lambda d: Namespace(**d))
    mocker.patch('chaos_agent.pods.list_all_pods', return_value=pod_list)

    pods = chaos_agent.pods.list_pods()

    expected_pod = 'kube-dns'
    expected_ns = 'kube-system'
    assert any([pod for pod in pods if expected_pod in pod[0]])
    assert any([pod for pod in pods if pod[1] == expected_ns])


def test_list_pods_with_inclusion(mocker):
    with open('./tests/mocks/pod-list.json', 'r') as f:
        raw_data = f.read()
        pod_list = json.loads(raw_data, object_hook=lambda d: Namespace(**d))
    mocker.patch('chaos_agent.pods.list_all_pods', return_value=pod_list)

    expected_pod = 'cert-manager-5c5f4b9b49-wcr4q'
    expected_ns = 'cert-manager'

    pods = chaos_agent.pods.list_pods(included_namespaces=[expected_ns])

    assert len(pods) == 1
    assert [pod[0] for pod in pods] == [expected_pod]
    assert [pod[1] for pod in pods] == [expected_ns]


def test_list_pods_with_exclusion(mocker):
    with open('./tests/mocks/pod-list.json', 'r') as f:
        raw_data = f.read()
        pod_list = json.loads(raw_data, object_hook=lambda d: Namespace(**d))
    mocker.patch('chaos_agent.pods.list_all_pods', return_value=pod_list)

    exclusion = ['ingress']
    expected_pod = 'nginx-ingress-controller-85744dcf89-2zc5j'
    expected_ns = 'ingress'

    pods = chaos_agent.pods.list_pods(excluded_namespaces=exclusion)

    assert expected_pod not in [pod for pod in pods]
    assert expected_ns not in [pod for pod in pods]


def test_list_pods_is_zero(mocker):
    mocker.patch('chaos_agent.pods.list_all_pods', return_value=None)
    pods = chaos_agent.pods.list_pods()
    assert pods is None


def test_list_all_pods(mocker):
    with open('./tests/mocks/pod-list.json', 'r') as f:
        raw_data = f.read()
        pod_list = json.loads(raw_data, object_hook=lambda d: Namespace(**d))
    mocker.patch('chaos_agent.pods.client.CoreV1Api.list_pod_for_all_namespaces', return_value=pod_list)

    all_pods = chaos_agent.pods.list_all_pods()
    parsed_pods = [pod.metadata.name for pod in all_pods.items]
    assert len(parsed_pods) == 13
    assert 'cert-manager-5c5f4b9b49-wcr4q' in parsed_pods


def test_list_all_pods_fails(mocker):
    mocker.patch('chaos_agent.pods.client.CoreV1Api.list_pod_for_all_namespaces', side_effect=ApiException('wibble'))
    all_pods = chaos_agent.pods.list_all_pods()
    assert all_pods is None


def test_select_one_random_pod(mocker):
    mock_pods = [['cert-manager-5c5f4b9b49-m6xd8', 'cert-manager'],
                 ['default-backend-66b68fd9d8-gxdzf', 'ingress'],
                 ['nginx-ingress-controller-85744dcf89-qt7t9', 'ingress'],
                 ['heapster-5fbbf8695b-qttnt', 'kube-system'],
                 ['heapster-v1.6.1-5b6bf6cc74-zfzgr', 'kube-system'],
                 ['kube-dns-795f7b8488-d65ps', 'kube-system'],
                 ['kube-proxy-gke-mw-prod-np-0-947e5a45-vpdd', 'kube-system']]

    stub_random_ints = mocker.patch('chaos_agent.pods.get_random_list_of_ints')

    stub_random_ints.return_value = [0]
    pod = chaos_agent.pods.select_random_pods(mock_pods)
    assert len(pod) == 1
    assert pod[0] == ('cert-manager-5c5f4b9b49-m6xd8', 'cert-manager')

    stub_random_ints.return_value = [6]
    pod = chaos_agent.pods.select_random_pods(mock_pods)
    assert len(pod) == 1
    assert pod[0] == ('kube-proxy-gke-mw-prod-np-0-947e5a45-vpdd', 'kube-system')


def test_select_three_random_pods(mocker):
    mock_pods = [['cert-manager-5c5f4b9b49-m6xd8', 'cert-manager'],
                 ['default-backend-66b68fd9d8-gxdzf', 'ingress'],
                 ['nginx-ingress-controller-85744dcf89-qt7t9', 'ingress'],
                 ['heapster-5fbbf8695b-qttnt', 'kube-system'],
                 ['heapster-v1.6.1-5b6bf6cc74-zfzgr', 'kube-system'],
                 ['kube-dns-795f7b8488-d65ps', 'kube-system'],
                 ['kube-proxy-gke-mw-prod-np-0-947e5a45-vpdd', 'kube-system']]

    stub_random_ints = mocker.patch('chaos_agent.pods.get_random_list_of_ints')

    stub_random_ints.return_value = [1, 3, 5]
    pod = chaos_agent.pods.select_random_pods(mock_pods)
    assert len(pod) == 3
    assert pod[0] == ('default-backend-66b68fd9d8-gxdzf', 'ingress')
    assert pod[1] == ('heapster-5fbbf8695b-qttnt', 'kube-system')
    assert pod[2] == ('kube-dns-795f7b8488-d65ps', 'kube-system')


def test_select_more_pods_than_available(mocker):
    mock_pods = [['cert-manager-5c5f4b9b49-m6xd8', 'cert-manager'],
                 ['default-backend-66b68fd9d8-gxdzf', 'ingress'],
                 ['nginx-ingress-controller-85744dcf89-qt7t9', 'ingress']]

    pod = chaos_agent.pods.select_random_pods(pods=mock_pods, num_pods=5)
    assert len(pod) == 3
    assert pod[0] == ('cert-manager-5c5f4b9b49-m6xd8', 'cert-manager')
    assert pod[1] == ('default-backend-66b68fd9d8-gxdzf', 'ingress')
    assert pod[2] == ('nginx-ingress-controller-85744dcf89-qt7t9', 'ingress')


def test_delete_pod(mocker, caplog, monkeypatch):
    monkeypatch.setenv('DEBUG', 'True')
    chaos_agent.utils.configure_logging()
    mocker.patch('chaos_agent.pods.client.CoreV1Api.delete_namespaced_pod')
    chaos_agent.pods.delete_pod(pod=('some-pod', 'some-namespace'))
    assert 'Deleted pod: some-pod in some-namespace' in caplog.text


def test_failed_delete_pod(mocker, caplog, monkeypatch):
    monkeypatch.setenv('DEBUG', 'True')
    chaos_agent.utils.configure_logging()
    stub_delete_pod = mocker.patch('chaos_agent.pods.client.CoreV1Api.delete_namespaced_pod')
    stub_delete_pod.side_effect = ApiException('wobble')
    chaos_agent.pods.delete_pod(pod=('some-pod', 'some-namespace'))
    assert 'Failed to delete pod, error message: (wobble)' in caplog.text

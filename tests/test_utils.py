import chaos_agent.utils as utils


# def test_load_k8s_context():
#     cfg = utils.load_k8s_context()
#     assert cfg == 1


def test_list_all_pods(caplog):
    pods = utils.list_all_pods()
    expected = "kube-proxy"
    matching_pods = [pod for pod in pods if expected in pod]
    assert len(matching_pods) > 0

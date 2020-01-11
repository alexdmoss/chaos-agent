import chaos_agent.nodes


def test_select_random_node(mocker):
    mock_nodes = ['gke-mw-prod-np-0-3be8d635-rwd1', 'gke-mw-prod-np-0-947e5a45-vpdd']

    stub_random_int = mocker.patch('chaos_agent.nodes.get_random_int')

    stub_random_int.return_value = 0
    node = chaos_agent.nodes.select_random_node(mock_nodes)
    assert node == 'gke-mw-prod-np-0-3be8d635-rwd1'

    stub_random_int.return_value = 1
    node = chaos_agent.nodes.select_random_node(mock_nodes)
    assert node == 'gke-mw-prod-np-0-947e5a45-vpdd'

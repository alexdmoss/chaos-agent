import chaos_agent.utils as utils
from pytest import raises
import yaml


def test_random():
    assert utils.get_random_int(10) in [i for i in range(10)]


def test_logging(monkeypatch, caplog):
    monkeypatch.setenv("DEBUG", "True")
    logger = utils.configure_logging()
    logger.debug("This is a DEBUG message")
    assert "This is a DEBUG message" in caplog.text


def test_load_good_config(tmp_path):
    mock_cfg = """
    dryRun: False # Set to True to just print the pod/node to be deleted, without taking action
    debug: True # This will print actions to log - they will be easier to spot!
    updateFrequency: 30 # How frequently it deletes pods/nodes
    randomiseFrequency: False # If set to True, it will randomly sleep for a time between 1->updateFrequency seconds
    numPodsToDelete: 2 # How many pods to delete per cycle. Set to 0 to skip, defaults to 1
    excludedNamespaces: # list of namespaces to ignore pods in. Defaults to kube-system
    - kube-system
    - default
    numNodesToDelete: 0 # How many nodes to delete per cycle. Set to 0 to skip [default]
    """

    mock_cfg_file = tmp_path / "tmp.yaml"
    mock_cfg_file.write_text(mock_cfg)

    config = utils.load_config(mock_cfg_file)

    assert config.dryRun is False
    assert config.debug is True
    assert config.updateFrequency == 30
    assert config.randomiseFrequency is False
    assert config.numPodsToDelete == 2
    assert config.excludedNamespaces == ['kube-system', 'default']
    assert config.numNodesToDelete == 0


def test_load_default_config(tmp_path):
    mock_cfg_file = tmp_path / "tmp.yaml"
    mock_cfg_file.write_text("")

    config = utils.load_config(mock_cfg_file)

    assert config.dryRun is True
    assert config.debug is False
    assert config.updateFrequency == 60
    assert config.randomiseFrequency is False
    assert config.numPodsToDelete == 1
    assert config.excludedNamespaces == ['kube-system']
    assert config.numNodesToDelete == 0


def test_load_bad_config_data(tmp_path, caplog):
    mock_cfg = """
    debug: "Yes"
    """
    mock_cfg_file = tmp_path / "tmp.yaml"
    mock_cfg_file.write_text(mock_cfg)

    config = utils.load_config(mock_cfg_file)

    assert "Default config values will be used" in caplog.text
    assert config.dryRun is True
    assert config.debug is False
    assert config.updateFrequency == 60


def test_load_irrelevant_config_data(tmp_path):
    mock_cfg = """
    someJunk: False # Set to True to just print the pod/node to be deleted, without taking action
    """
    mock_cfg_file = tmp_path / "tmp.yaml"
    mock_cfg_file.write_text(mock_cfg)

    config = utils.load_config(mock_cfg_file)

    assert config.dryRun is True
    assert config.debug is False
    assert config.updateFrequency == 60


def test_load_partial_config_data(tmp_path):
    mock_cfg = """
    updateFrequency: 30
    """
    mock_cfg_file = tmp_path / "tmp.yaml"
    mock_cfg_file.write_text(mock_cfg)

    config = utils.load_config(mock_cfg_file)

    assert config.dryRun is True
    assert config.debug is False
    assert config.updateFrequency == 30


def test_load_invalid_yaml_config(tmp_path, caplog):
    mock_cfg = """
    bob:
    thebuilder
    """
    mock_cfg_file = tmp_path / "tmp.yaml"
    mock_cfg_file.write_text(mock_cfg)

    config = utils.load_config(mock_cfg_file)

    assert "Failed to parse config yaml" in caplog.text
    assert "Default config values will be used" in caplog.text
    assert config.dryRun is True
    assert config.debug is False
    assert config.updateFrequency == 60


def test_load_weird_yaml_config(tmp_path, caplog):
    mock_cfg = """
    a:b:c:d
    """
    mock_cfg_file = tmp_path / "tmp.yaml"
    mock_cfg_file.write_text(mock_cfg)

    config = utils.load_config(mock_cfg_file)

    assert "Default config values will be used" in caplog.text
    assert config.dryRun is True
    assert config.debug is False
    assert config.updateFrequency == 60


def test_missing_yaml_config(tmp_path, caplog):

    config = utils.load_config("/invalid/path.yaml")

    assert "Default config values will be used" in caplog.text
    assert config.dryRun is True
    assert config.debug is False
    assert config.updateFrequency == 60

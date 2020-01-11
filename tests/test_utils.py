import chaos_agent.utils as utils


def test_random():
    assert utils.get_random_int(10) in [i for i in range(10)]


def test_logging(monkeypatch, caplog):
    monkeypatch.setenv("DEBUG", "True")
    logger = utils.configure_logging()
    logger.debug("This is a DEBUG message")
    assert "This is a DEBUG message" in caplog.text

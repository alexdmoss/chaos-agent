import main


def test_main(caplog, mocker):
    mocker.patch('main.load_k8s_context')
    mocker.patch('main.find_and_terminate_pods')
    main.main()
    assert "BEHOLD" in caplog.text


def test_init(mocker):
    mocker.patch.object(main, "main", return_value=42)
    mocker.patch.object(main, "__name__", "__main__")
    mocker.patch.object(main.sys, "exit")
    main.init()
    assert main.sys.exit.call_args[0][0] == 42

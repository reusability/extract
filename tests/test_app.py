from .context import src


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    a = src.App()
    a.Run()
    # captured = capsys.readouterr()
    # assert "Hello World..." in captured.out

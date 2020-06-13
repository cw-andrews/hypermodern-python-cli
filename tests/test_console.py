import click.testing
import pytest

from hypermodern_python_cli import console


@pytest.fixture
def cli_test_runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


def test_main_succeeds(cli_test_runner, mock_requests_get):
    result = cli_test_runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(cli_test_runner, mock_requests_get):
    result = cli_test_runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(cli_test_runner, mock_requests_get):
    cli_test_runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(cli_test_runner, mock_requests_get):
    cli_test_runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(cli_test_runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = cli_test_runner.invoke(console.main)
    assert result.exit_code == 1

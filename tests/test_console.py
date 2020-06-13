import click.testing
import pytest
import requests

from hypermodern_python_cli import console


@pytest.fixture
def cli_test_runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("hypermodern_python_cli.wikipedia.random_page")


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


def test_main_prints_messages_on_request_error(cli_test_runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = cli_test_runner.invoke(console.main)
    assert "Error" in result.output


def test_main_uses_specified_language(cli_test_runner, mock_wikipedia_random_page):
    cli_test_runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(cli_test_runner):
    result = cli_test_runner.invoke(console.main)
    assert result.exit_code == 0

import pytest
from common.seleniumwrapper import init, login_routine

def pytest_addoption(parser):
    parser.addoption("--env", action="append", default=[], help=("test environment defined in config.cfg"))
    parser.addoption("--host", action="append", default=[], help=("host (incl. port) of webdriver"))
    parser.addoption("--webdriver", action="append", default=[], help=("which webdriver to use"))
    parser.addoption("--frontend_url", action="append", default=[], help=("frontend url to use"))


@pytest.fixture
def cli_env(request):
    environment = request.config.getoption("--env")
    if environment:
        return environment[0]
    raise Exception("No environment passed")


@pytest.fixture
def cli_host(request):
    host = request.config.getoption("--host")
    if host:
        return host[0]
    raise Exception("No host passed")


@pytest.fixture
def cli_webdriver(request):
    webdriver = request.config.getoption("--webdriver")
    if webdriver:
        return webdriver[0]
    raise Exception("No webdriver passed")

@pytest.fixture
def cli_frontend_url(request):
    environment = request.config.getoption("--frontend_url")
    if environment:
        return environment[0]
    raise Exception("No environment passed")


@pytest.fixture
def config_parser():
    import os
    import configparser
    config_parser = configparser.ConfigParser()
    config_file_path = os.path.dirname(os.path.abspath(__file__)) + '/config/config.cfg'
    config_parser.read(config_file_path)
    return config_parser


@pytest.fixture
def get_config(cli_env, config_parser):
    def get_key_for_env(key):
        return config_parser.get(cli_env, key)

    return get_key_for_env


@pytest.fixture
def test_user(get_config, cli_env):
    username = get_config("username")
    password = get_config("password")
    return {
        "username": username,
        "password": password
    }


@pytest.fixture
def env_options(cli_env, config_parser):
    return config_parser.get(cli_env)

@pytest.fixture
def base_url(get_config, cli_frontend_url):
    if cli_frontend_url:
        return cli_frontend_url
    return get_config("url")


@pytest.fixture(scope="function")
def browser(cli_host, cli_webdriver):
    from splinter import Browser
    driver = Browser(driver_name="remote", url=cli_host, browser=cli_webdriver)
    yield driver
    driver.quit()

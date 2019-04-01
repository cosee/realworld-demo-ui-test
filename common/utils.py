import sys
import os
from selenium import webdriver
from conftest import configParser
from pyvirtualdisplay import Display
import logging
from selenium.webdriver.remote.remote_connection import LOGGER


def get_argument(field):
    if len(sys.argv) > 2:
        for argument in sys.argv:
            temp = argument.strip('-')
            if (temp.startswith(field)):
                arguments = temp.split("=")
                if len(arguments) > 1:
                    return arguments[1]
                return True
    environment_variable = os.environ.get(field)
    if environment_variable is None:
        return ""
    if environment_variable is 'True':
        return True
    elif environment_variable is 'False':
        return False
    return environment_variable


def get_base_url(env):
    if env == 'aws':
        return os.environ.get('frontend_url')
    return get_config_value_by_env_key(env, 'url')


def get_config_value_by_env_key(env, key):
    config_parser = ConfigParser.ConfigParser()
    config_file_path = os.path.dirname(os.path.abspath(__file__)) + '/../config/config.cfg'
    config_parser.read(config_file_path)
    return config_parser.get(env, key)


def resolveRemoteWebdriverType():
    webdriverType = get_argument("webdriver")
    if webdriverType == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        return chrome_options
    elif webdriverType == "chrome-headless":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        return chrome_options
    else:
        return webdriver.ChromeOptions()


def resolveLocalWebdriverType():
    webdriverType = get_argument("webdriver")
    if webdriverType == "chrome":
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--start-maximized") # currently buggy in chrome v. 69+ and chromedriver v 2.40+
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(chrome_options=chrome_options)
    elif webdriverType == "chrome-incognito":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        return webdriver.Chrome(chrome_options=chrome_options)
    elif webdriverType == "chrome-headless":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(chrome_options=chrome_options)
    elif webdriverType == "firefox":
        return webdriver.Firefox()
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        return webdriver.Chrome(chrome_options=chrome_options)


def get_config_value_by_env(config_parser, env, key):
    return config_parser.get(env, key)


def get_throttle_factor():
    throttle_factor_string = get_argument('T') or get_argument('throttle') or '1'
    return float(throttle_factor_string)


def get_config_value(key):
    environment = configParser().get('test', 'env')
    if len(sys.argv) > 2:
        environment = get_argument("env")
        environment = environment if len(environment) > 0 else configParser.get('test', 'env')
    return configParser().get(environment, key)


def connect_driver():
    useVirtualDisplay = get_argument('useVirtualDisplay')
    if useVirtualDisplay is not (None or ""):
        displayHeight = get_argument('displayHeight')
        displayWidth = get_argument('displayWidth')
        if displayHeight is None or displayWidth is None:
            raise Exception("Please provide displayHeight and displayWidth when using virtualDisplay")
        display = Display(visible=0, size=(displayWidth, displayHeight))
        display.start()
    url = get_base_url(get_argument('env'))
    driver = None
    remote = get_argument("remote")
    host = get_argument("host")
    webdriverType = resolveRemoteWebdriverType()
    LOGGER.setLevel(logging.WARNING)
    if remote and host != "":
        driver = webdriver.Remote(command_executor=host, desired_capabilities=webdriverType.to_capabilities())
    else:
        driver = resolveLocalWebdriverType()
    driver.get(url)
    return driver

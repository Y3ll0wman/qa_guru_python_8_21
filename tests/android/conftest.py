import pytest
from appium.options.android import UiAutomator2Options
from selene import browser
from dotenv import load_dotenv
import os

from selenium import webdriver


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    username = os.getenv('USER_NAME')
    access_key = os.getenv('ACCESS_KEY')
    remote_browser_url = os.getenv('REMOTE_BROWSER_URL')

    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        "platformName": "android",
        "platformVersion": "13.0",
        "deviceName": "Samsung Galaxy S23 Ultra",

        # Set URL of the application under test
        "app": "bs://sample.app",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "Android tests",
            "buildName": "browserstack-wikipedia-build",
            "sessionName": "BStack wikipedia_test",

            # Set your access credentials
            "userName": username,
            "accessKey": access_key
        }
    })

    # browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)
    browser.config.driver_remote_url = remote_browser_url
    browser.config.driver_options = options
    browser.config.timeout = 10.0

    yield

    browser.quit()

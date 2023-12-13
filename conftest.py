import allure
import allure_commons
import pytest
import os
import requests

from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser, support
from dotenv import load_dotenv
from appium import webdriver


@pytest.fixture(scope='function', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function')
def android_mobile_management():
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

    # browser.config.driver_remote_url = remote_browser_url
    # browser.config.driver_options = options

    with allure.step('setup app session'):
        browser.config.driver = webdriver.Remote(
            remote_browser_url,
            options=options
        )

    browser.config.timeout = 10.0

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG
    )

    allure.attach(
        browser.driver.page_source,
        name='page_source_xml',
        attachment_type=allure.attachment_type.XML
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(username, access_key)
    ).json()

    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML
    )


@pytest.fixture(scope='function')
def ios_mobile_management():
    username = os.getenv('USER_NAME')
    access_key = os.getenv('ACCESS_KEY')
    remote_browser_url = os.getenv('REMOTE_BROWSER_URL')

    options = XCUITestOptions().load_capabilities({
        # Specify device and os_version for testing
        "platformName": "ios",
        "platformVersion": "16",
        "deviceName": "iPhone 14 Pro Max",

        # Set URL of the application under test
        "app": "bs://444bd0308813ae0dc236f8cd461c02d3afa7901d",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "Ios tests",
            "buildName": "browserstack-simple-app-build",
            "sessionName": "BStack Simple app test",

            # Set your access credentials
            "userName": username,
            "accessKey": access_key
        }
    })

    # browser.config.driver_remote_url = remote_browser_url
    # browser.config.driver_options = options

    with allure.step('setup app session'):
        browser.config.driver = webdriver.Remote(
            remote_browser_url,
            options=options
        )

    browser.config.timeout = 10.0

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG
    )

    allure.attach(
        browser.driver.page_source,
        name='page_source_xml',
        attachment_type=allure.attachment_type.XML
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

        bstack_session = requests.get(
            f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
            auth=(username, access_key)
        ).json()

    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML
    )

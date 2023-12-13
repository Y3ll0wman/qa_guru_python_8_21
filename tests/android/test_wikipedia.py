import pytest

from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


def test_search(android_mobile_management):
    # WHEN
    with step('Press Skip button'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')).click()

    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type('Appium')

    # THEN
    with step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_open_article(android_mobile_management):
    # WHEN
    with step('Press Skip button'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')).click()

    with step('Search article'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type('Appium')
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).click()

    # THEN
    with step('Verify article title'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Appium'))

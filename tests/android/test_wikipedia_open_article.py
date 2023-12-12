import pytest
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


@pytest.mark.xfail
def test_open_article():
    # WHEN
    with step('Search article'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")).click()

    # THEN
    with step('Verify article found'):
        results = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/pcs"))
        results.should(have.text('Appium'))

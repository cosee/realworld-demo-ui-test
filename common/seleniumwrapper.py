from pytest import fixture

from common.constants.loginconstants import LOGIN_URL, XPATH_EMAIL_INPUT, XPATH_PASSWORD_INPUT, XPATH_SUBMIT


@fixture
def init(browser, base_url):
    browser.visit(base_url)


@fixture
def login_routine(browser, base_url, test_user):
    print (base_url + LOGIN_URL)
    browser.visit(base_url + LOGIN_URL)

    browser.is_element_visible_by_xpath(XPATH_EMAIL_INPUT)
    email_input = browser.find_by_xpath(XPATH_EMAIL_INPUT)
    email_input.first.type(test_user["username"])

    browser.is_element_visible_by_xpath(XPATH_PASSWORD_INPUT)
    pw_input = browser.find_by_xpath(XPATH_PASSWORD_INPUT)
    pw_input.first.type(test_user["password"])

    submit_btn = browser.find_by_xpath(XPATH_SUBMIT)
    submit_btn.first.click()

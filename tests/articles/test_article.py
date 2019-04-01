from common.constants.article import XPATH_ARTICLE_TITLE, CREATE_ARTICLE_PAGE, XPATH_ARTICLE_ABOUT, \
    XPATH_ARTICLE_CONTENT, XPATH_ARTICLE_OVERVIEW_TITLE, XPATH_ARTICLE_SUBMIT


def test_create_article(login_routine, browser, base_url):
    browser.visit(base_url + CREATE_ARTICLE_PAGE)

    browser.is_element_visible(browser.find_by_xpath, XPATH_ARTICLE_TITLE)
    title = browser.find_by_xpath(XPATH_ARTICLE_TITLE)
    title.first.type("some title")

    browser.is_element_visible(browser.find_by_xpath, XPATH_ARTICLE_ABOUT)
    about = browser.find_by_xpath(XPATH_ARTICLE_ABOUT)
    about.first.type("about something")

    browser.is_element_visible(browser.find_by_xpath, XPATH_ARTICLE_CONTENT)
    content = browser.find_by_xpath(XPATH_ARTICLE_CONTENT)
    content.first.type("very important")

    browser.is_element_visible(browser.find_by_xpath, XPATH_ARTICLE_SUBMIT)
    submit_btn = browser.find_by_xpath(XPATH_ARTICLE_SUBMIT)
    submit_btn.first.click()

    browser.is_element_not_present(browser.find_by_xpath, XPATH_ARTICLE_SUBMIT)

    browser.is_element_visible(browser.find_by_xpath, XPATH_ARTICLE_OVERVIEW_TITLE)
    title = browser.find_by_xpath(XPATH_ARTICLE_OVERVIEW_TITLE)

    assert ("some title" in title.first.text )
    assert ("article/some-title" in browser.url)

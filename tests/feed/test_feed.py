import pytest

from common.constants.feed import FEED_PAGE, XPATH_ARTICLE_CONTAINER, XPATH_LAST_ARTICLE_CONTAINER, \
    XPATH_FIRST_ARTICLE_CONTAINER, XPATH_ARTICLE_HEADER, XPATH_PAGE_ITEMS


@pytest.mark.repeat(100)
def test_feed_has_ten_articles(browser, base_url):
    browser.visit(base_url + FEED_PAGE)
    browser.is_element_visible(browser.find_by_xpath, XPATH_LAST_ARTICLE_CONTAINER)

    articles = browser.find_by_xpath(XPATH_ARTICLE_CONTAINER)
    assert (len(articles) is 10)


def test_feed_has_first_article(browser, base_url):
    browser.visit(base_url + FEED_PAGE)
    browser.is_element_visible(browser.find_by_xpath, XPATH_FIRST_ARTICLE_CONTAINER)

    header = browser.find_by_xpath(XPATH_FIRST_ARTICLE_CONTAINER + XPATH_ARTICLE_HEADER)
    assert ("hahaha" in header.first.text)


def test_feed_has_fifty_pages(browser, base_url):
    browser.visit(base_url + FEED_PAGE)
    browser.is_element_visible(browser.find_by_xpath, XPATH_LAST_ARTICLE_CONTAINER)

    page_items = browser.find_by_xpath(XPATH_PAGE_ITEMS)
    assert (len(page_items) is 50)

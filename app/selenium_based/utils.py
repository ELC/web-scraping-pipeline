from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


chrome_driver = ChromeDriverManager().install()


@contextmanager
def get_driver() -> webdriver.Chrome:
    options = Options()

    pref = {"profile.default_content_setting_values.notifications": 2}
    options.add_argument("window-size=1840,1050")
    options.add_experimental_option("prefs", pref)

    try:
        driver = webdriver.Chrome(chrome_driver, options=options)
        yield driver
    finally:
        driver.quit()


options = Options()
pref = {"profile.default_content_setting_values.notifications": 2}
options.add_argument("window-size=1840,1050")
options.add_experimental_option("prefs", pref)

singleton_driver = webdriver.Chrome(chrome_driver, options=options)


@contextmanager
def get_singleton_driver() -> webdriver.Chrome:
    yield singleton_driver


def close_singleton_driver() -> None:
    singleton_driver.quit()


@contextmanager
def get_headless_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")

    try:
        driver = webdriver.Chrome(chrome_driver, options=options)
        yield driver
    finally:
        driver.quit()

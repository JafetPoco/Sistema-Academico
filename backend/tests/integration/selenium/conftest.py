import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver():
    """Provide a Chrome driver that works locally or against a remote Selenium hub."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    remote_url = os.getenv("SELENIUM_REMOTE_URL")
    if remote_url:
        driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        driver = webdriver.Chrome(service=Service(), options=options)

    driver.set_window_size(1440, 900)

    yield driver
    driver.quit()

import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def setup_teardown():

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn")

    yield driver

    driver.quit()

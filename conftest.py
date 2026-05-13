# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import time

@pytest.fixture
def driver():
    # Khởi tạo trình duyệt một lần duy nhất cho mỗi bài test
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    
    # Tự động đóng sau khi test xong (Teardown)
    time.sleep(5)
    driver.quit()

@pytest.fixture
def wait(driver):
    # Cung cấp bộ đợi 15s cho các bài test
    return WebDriverWait(driver, 15)
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from constants import BASE_URL, EMAIL, PASSWORD


def login_email_password(driver, wait):
    driver.get(BASE_URL)
    login_homepage_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
    login_homepage_btn.click()
    email_password_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login with Email and Password")))
    email_password_option.click()
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys(EMAIL)
    password_field = driver.find_element(By.NAME, "login_password")
    password_field.send_keys(PASSWORD)
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "sendOtpBtn")))
    login_btn.click()


def test_mezon_login_success():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()
    driver.maximize_window()                            # Mở toàn màn hình để dễ tìm Element
    wait = WebDriverWait(driver, 15)             # Thiết lập bộ đếm thời gian chờ tối đa 15s

    try:
        login_email_password(driver, wait)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))
        print("Login Successfully!")


    except Exception as e:
        print(f"RESULT: Failed due to - {e}")
        # Chụp màn hình lúc lỗi để điều tra
        driver.save_screenshot("evidence/error_login.png")

    finally:
        time.sleep(5)
        driver.quit()
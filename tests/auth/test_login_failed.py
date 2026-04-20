import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_mezon_login_failed():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()
    driver.maximize_window()                            # Mở toàn màn hình để dễ tìm Element
    wait = WebDriverWait(driver, 15)             # Thiết lập bộ đếm thời gian chờ tối đa 15s
    try:
        driver.get("https://mezon.ai/")  # Truy cập Mezon
        login_homepage_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        login_homepage_btn.click()
        email_password_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login with Email and Password")))
        email_password_option.click()
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys("yocosa3965@crsay.com")
        password_field = driver.find_element(By.NAME, "login_password")
        password_field.send_keys("Thanhhien312@@")
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "sendOtpBtn")))
        login_btn.click()
        error_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='alert']")))
        actual_message = error_element.text
        print("The actual result is: "+ actual_message)
        expected_message = "Could not verify email or password"
        assert expected_message == actual_message, "Error: Expect " + expected_message + " but the actual result is " + actual_message
        print("Confirm: Error message displays correctly!")



    except Exception as e:
        print(f"RESULT: Failed due to - {e}")
        # Chụp màn hình lúc lỗi để điều tra
        driver.save_screenshot("evidence/error_login_failed.png")

    finally:
        time.sleep(5)
        driver.quit()

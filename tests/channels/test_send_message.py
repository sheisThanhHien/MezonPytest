import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import BASE_URL, EMAIL, PASSWORD

import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Gọi hàm để lấy đối tượng thời gian chính xác tại thời điểm mã được thực thi (bao gồm năm, tháng, ngày, giờ, phút, giây và micro giây).

def test_send_message():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    try:
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
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='flex flex-row gap-2 items-center text-theme-primary-active font-medium']")))
        print("Login Successfully!")

        clan_test = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='MEZON HEHE 1']//img[@placeholder='clan']")))
        clan_test.click()
        channel = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='1970339269465608192-1970339269482385408']")))
        channel.click()
        chat_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='editorReactMentionChannel']")))
        my_message = "Hello Mezon at " + now
        chat_input.send_keys(my_message)
        chat_input.send_keys(Keys.ENTER)

        time.sleep(2)  # đợi tin nhắn hiện lên

        messages = driver.find_elements(By.XPATH, "/html[1]/body[1]/div[2]/div[2]/div[2]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[58]/div[1]/div[1]")
        last_message_text = messages[-1].text
        print("The last text is " + last_message_text)

        assert my_message == last_message_text, "Error: Messages are not matched!!!"
        print("Test send message successfully!!")


    except Exception as e:
        print(f"RESULT: Failed due to - {e}")
        # Chụp màn hình lúc lỗi để điều tra
        driver.save_screenshot("evidence/test_send_message.png")

    finally:
        time.sleep(5)
        driver.quit()
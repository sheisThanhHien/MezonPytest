# helpers.py
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from constants import BASE_URL, EMAIL, PASSWORD

import datetime

def get_current_time(): 
    return datetime.datetime.now().strftime("%Y%m%d %H%M%S")                # logic xử lý time

# def login_email_password(driver, wait):
#     driver.get(BASE_URL)
#     wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
#     wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login with Email and Password"))).click()
#     wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
#     driver.find_element(By.NAME, "login_password").send_keys(PASSWORD)
#     wait.until(EC.element_to_be_clickable((By.ID, "sendOtpBtn"))).click()
#     wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))
        


# def find_message_item(driver, expected_text):
#     # Hàm tìm tin nhắn lấy từ test_send_message.py
#     message_items = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='message-item']")    
#     for item in reversed(message_items):
#         text_nodes = item.find_elements(By.XPATH, ".//div[contains(@class,'text-theme-message')]")
#         if text_nodes and text_nodes[0].text.strip() == expected_text:
#             return item, text_nodes[0]
#     return None, None


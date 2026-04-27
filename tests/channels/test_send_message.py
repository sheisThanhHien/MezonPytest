import time
import traceback
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.auth.test_login_success import login_email_password

from constants import get_current_time

def find_message_item_by_text(driver, expected_text):
    message_items = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='message-item']")    
    for item in reversed(message_items):
        text_nodes = item.find_elements(By.XPATH, ".//div[contains(@class,'text-theme-message')]")
        if not text_nodes:
            continue
        text_value = text_nodes[0].text.strip()
        if text_value == expected_text:
            return item, text_nodes[0]
    return None, None


def test_send_message():
   
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    try:
        login_email_password(driver, wait)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))
        print("Login Successfully!")

        clan_test = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-clan_item']")))
        clan_test.click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']")))
        first_channel = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']")[0]
        first_channel.click()
        chat_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='editorReactMentionChannel']")))
        my_message = "Pytest Mezon at " + get_current_time()
        chat_input.send_keys(my_message)
        chat_input.send_keys(Keys.ENTER)

        time.sleep(2)  # đợi tin nhắn hiện lên

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='message-item']")))

        matched_item = None
        matched_text_node = None
        deadline = time.time() + 120

        while time.time() < deadline:
            matched_item, matched_text_node = find_message_item_by_text(driver, my_message)
            if matched_item is None:
                time.sleep(1)
                continue

            matched_item_class = matched_item.get_attribute("class") or ""
            matched_text_class = matched_text_node.get_attribute("class") or ""

            # Error state xuất hiện rõ trên message-item.
            if "is-error" in matched_item_class:
                raise AssertionError(
                    "Error: Message send failed (message-item has class 'is-error'). "
                    f"Message text: {my_message}"
                )

            # Success khi không còn trạng thái sending.
            is_sending = "pointer-events-none" in matched_item_class or "opacity-50" in matched_text_class
            if not is_sending:
                break

            time.sleep(1)

        assert matched_item is not None and matched_text_node is not None, (
            f"Error: Could not find sent message item with text '{my_message}'."
        )

        final_item_class = matched_item.get_attribute("class") or ""
        final_text_class = matched_text_node.get_attribute("class") or ""
        final_message_text = matched_text_node.text.strip()
        print("The last matched text is " + final_message_text)

        assert "is-error" not in final_item_class, (
            "Error: Message send failed (message-item has class 'is-error'). "
            f"Message text: {final_message_text}"
        )
        assert "pointer-events-none" not in final_item_class and "opacity-50" not in final_text_class, (
            "Error: Message is still in sending status after waiting 30s."
        )
        assert my_message == final_message_text, "Error: Messages are not matched!!!"
        print("Test send message successfully!!")


    except Exception as e:
        print(f"RESULT: Failed due to - {repr(e)}")
        traceback.print_exc()
        # Chụp màn hình lúc lỗi để điều tra
        driver.save_screenshot("evidence/test_send_message.png")
        raise

    finally:
        time.sleep(5)
        driver.quit()
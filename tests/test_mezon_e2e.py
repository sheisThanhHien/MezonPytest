from helpers import get_current_time, login_email_password, create_clan, delete_clan

import time
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_mezon_full_flow(driver, wait):
    try:
        # Login
        login_email_password(driver, wait)
        
        
        # Create Clan
        clan_name = create_clan(driver, wait)
        header_clan_name = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))
            ).text.strip()
        print("Header clan name is " + header_clan_name)
        assert header_clan_name == clan_name.upper(), (
                f"Clan name mismatch. Expected '{clan_name.upper()}', got '{header_clan_name}'."
            )

        print("Created clan successfully.")

        # # Gửi tin nhắn 
        # # Chọn channel đầu tiên
        # channels = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']")))
        # channels[0].click()
        
        # chat_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='editorReactMentionChannel']")))
        # msg_content = "Pytest Mezon at " + get_current_time()
        # chat_input.send_keys(msg_content + Keys.ENTER)
        
        # # Kiểm tra trạng thái tin nhắn
        # time.sleep(2)
        # matched_item, matched_text = find_message_item(driver, msg_content)
        # assert matched_item is not None, "Lỗi: Không tìm thấy tin nhắn đã gửi!"
        # assert "is-error" not in matched_item.get_attribute("class"), "Lỗi: Tin nhắn bị mark lỗi gửi!"



        # Delete Clan
        delete_clan(driver, wait, clan_name)
 
    except Exception as e:
        # Chụp ảnh màn hình khi lỗi để dễ debug
        driver.save_screenshot(f"evidence/error_flowe2e_{get_current_time()}.png")
        print(f"Flow failed: {repr(e)}")
        raise e         # Re-raise để pytest ghi nhận là test FAIL
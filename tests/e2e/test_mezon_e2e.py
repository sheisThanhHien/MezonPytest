# from helpers import get_current_time, login_email_password, create_clan, delete_clan
# from tests.categories.test_create_category import create_category

# import time
# import pytest
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# from flows.clan_flow import create_clan
# from flows.auth_flow import login_email_password
# from flows.category_flow import create_category

# def test_mezon_full_flow(driver, wait):
#     try:
#         # Login
#         login_email_password(driver, wait)
        
        
#         # Create Clan
#         clan_name = create_clan(driver, wait)
#         header_clan_name = wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))
#             ).text.strip()
#         print("Header clan name is " + header_clan_name)
#         assert header_clan_name == clan_name.upper(), (
#                 f"Clan name mismatch. Expected '{clan_name.upper()}', got '{header_clan_name}'."
#             )

#         print("Created clan successfully.")


#         # Create Category
#         create_category(driver, wait)



#         # # Gửi tin nhắn 
#         # # Chọn channel đầu tiên
#         # channels = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']")))
#         # channels[0].click()
        
#         # chat_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='editorReactMentionChannel']")))
#         # msg_content = "Pytest Mezon at " + get_current_time()
#         # chat_input.send_keys(msg_content + Keys.ENTER)
        
#         # # Kiểm tra trạng thái tin nhắn
#         # time.sleep(2)
#         # matched_item, matched_text = find_message_item(driver, msg_content)
#         # assert matched_item is not None, "Lỗi: Không tìm thấy tin nhắn đã gửi!"
#         # assert "is-error" not in matched_item.get_attribute("class"), "Lỗi: Tin nhắn bị mark lỗi gửi!"



#         # Delete Clan
#         delete_clan(driver, wait, clan_name)

        
 
#     except Exception as e:
#         # Chụp ảnh màn hình khi lỗi để dễ debug
#         driver.save_screenshot(f"evidence/error_flowe2e_{get_current_time()}.png")
#         print(f"Flow failed: {repr(e)}")
#         raise e         # Re-raise để pytest ghi nhận là test FAIL


from selenium.webdriver.common.by import By

from flows.auth_flow import login_email_password

from flows.clan_flow import (create_clan,delete_clan)

from flows.category_flow import (create_category,edit_category)

from utils.helpers import get_current_time

def test_mezon_full_flow(driver, wait):

    # LOGIN
    login_email_password(driver, wait)

    # CREATE CLAN
    clan_name = create_clan(driver, wait)
    assert clan_name is not None

    # CREATE CATEGORY
    category_name = create_category(driver, wait)

    assert category_name is not None

    # # EDIT CATEGORY
    # edited_category_name = ("Category Edited " + get_current_time())

    # edit_category(driver,wait, category_name, edited_category_name)

    # # VERIFY CATEGORY EDITED
    # category_containers = driver.find_elements(By.CSS_SELECTOR,"[data-e2e='clan_page-side_bar-channel_list-category']")
    # is_found = False
    # target_name = edited_category_name.upper()
    # for container in category_containers:
    #     try:
    #         name_element = container.find_element(
    #             By.CSS_SELECTOR,
    #             "[data-e2e='clan_page-side_bar-channel_list-category-name']"
    #         )

    #         actual_name = name_element.text.strip().upper()

    #         if target_name in actual_name:
    #             is_found = True
    #             break
    #     except:
    #         continue

    # assert is_found, (
    #     f"Cannot find edited category '{target_name}'"
    # )

    # CLEANUP
    delete_clan(driver, wait, clan_name)
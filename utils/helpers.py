# helpers.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from constants import BASE_URL, EMAIL, PASSWORD

import datetime

def get_current_time(): 
    return datetime.datetime.now().strftime("%Y%m%d %H%M%S")                # logic xử lý time

def login_email_password(driver, wait):
    driver.get(BASE_URL)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login with Email and Password"))).click()
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "login_password").send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.ID, "sendOtpBtn"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))


def create_clan(driver, wait):
        create_clan_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-button-add_clan']"))).click()

        create_clan_modal = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan']")))
        print("Opened modal clan creation successfully.")

        option_create_my_own = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-template-item-create_my_own']"))).click()
        
        modal_clan_name_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-input-clan_name']")))
        clan_name = "E2E Clan " + get_current_time()
        modal_clan_name_input.send_keys(clan_name)

        buttons = create_clan_modal.find_elements(By.CSS_SELECTOR, "button[data-e2e='button-base']")
        assert len(buttons) >= 2, "Expected Back and Create buttons in create clan modal."
        modal_clan_create_btn = buttons[-1]                         # footer button bên phải
        wait.until(lambda d: modal_clan_create_btn.is_enabled())
        modal_clan_create_btn.click()
        print("Clan created successfully!")
        
        return clan_name

        


def find_message_item(driver, expected_text):
    # Hàm tìm tin nhắn lấy từ test_send_message.py
    message_items = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='message-item']")    
    for item in reversed(message_items):
        text_nodes = item.find_elements(By.XPATH, ".//div[contains(@class,'text-theme-message')]")
        if text_nodes and text_nodes[0].text.strip() == expected_text:
            return item, text_nodes[0]
    return None, None

def delete_clan (driver, wait, clan_name):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))).click()    
    clan_settings_menu = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']")))
    clan_settings_option = clan_settings_menu[3].click() 
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-settings-sidebar-delete']"))).click() 
    confirm_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-input']")))
    confirm_input.send_keys(clan_name)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-confirm']"))).click() 
    print("Deleted clan successfully.")    
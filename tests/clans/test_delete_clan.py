import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from helpers import get_current_time, login_email_password, create_clan, delete_clan

def delete_clan (driver, wait, clan_name):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))).click()    
    clan_settings_menu = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']")))
    clan_settings_option = clan_settings_menu[3].click() 
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-settings-sidebar-delete']"))).click() 
    confirm_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-input']")))
    confirm_input.send_keys(clan_name)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-confirm']"))).click() 
    print("Deleted clan successfully.")    


def test_delete_clan():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    try:
        # Login
        login_email_password(driver, wait)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))
        print("Login Successfully!")

        # Create Clan
        # create_clan(driver, wait)
        clan_name = create_clan(driver, wait)

        # Delete clan
        delete_clan(driver, wait, clan_name)

        time.sleep(3)
        

    except Exception as e:
        print(f"RESULT: Failed due to - {repr(e)}")
        driver.save_screenshot("evidence/test_delete_clan.png")
        raise        

    finally:
        time.sleep(7)
        driver.quit()    

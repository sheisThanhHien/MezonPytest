import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.auth.test_login_success import login_email_password
from constants import get_current_time


def test_create_clan():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    try:
        # Reuse login flow 
        login_email_password(driver, wait)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))
        print("Login Successfully!")

        create_clan_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-button-add_clan']")))
        create_clan_btn.click()

        create_clan_modal = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan']")))
        print("Opened modal clan creation successfully.")

        option_create_my_own = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-template-item-create_my_own']")))
        option_create_my_own.click()
        
        modal_clan_name_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-input-clan_name']")))
        clan_name = "Pytest Mezon at " + get_current_time()
        modal_clan_name_input.send_keys(clan_name)

        buttons = create_clan_modal.find_elements(By.CSS_SELECTOR, "button[data-e2e='button-base']")
        assert len(buttons) >= 2, "Expected Back and Create buttons in create clan modal."
        modal_clan_create_btn = buttons[-1]  # footer button bên phải
        wait.until(lambda d: modal_clan_create_btn.is_enabled())
        modal_clan_create_btn.click()

        header_clan_name = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))
        ).text.strip()
        print("Header clan name is " + header_clan_name)
        assert header_clan_name == clan_name.upper(), (
            f"Clan name mismatch. Expected '{clan_name.upper()}', got '{header_clan_name}'."
        )

        print("Created clan successfully.")
        
        

    except Exception as e:
        print(f"RESULT: Failed due to - {repr(e)}")
        driver.save_screenshot("evidence/test_create_clan.png")
        raise

    finally:
        time.sleep(3)
        driver.quit()

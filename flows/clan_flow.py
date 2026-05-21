from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages import clancreation_page
from pages.clancreation_page import CreateClanModal

from utils.helpers import get_current_time


def create_clan(driver, wait):

    clancreation_page = CreateClanModal(driver, wait)
    clancreation_page.click_create_clan_button()
    clancreation_page.click_create_my_own_option()
    clan_name = "E2E Clan " + get_current_time()
    clancreation_page.input_clan_name(clan_name)
    clancreation_page.click_confirm_create_clan()

    return clan_name    
    

    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-button-add_clan']"))).click()
    # create_clan_modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan']")))
    # option_create_my_own = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-template-item-create_my_own']")))
    # option_create_my_own.click()
    # modal_clan_name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-input-clan_name']")))
    # clan_name = "E2E Clan " + get_current_time()
    # modal_clan_name_input.send_keys(clan_name)
    # buttons = create_clan_modal.find_elements(
    #     By.CSS_SELECTOR,
    #     "button[data-e2e='button-base']"
    # )
    # assert len(buttons) >= 2
    # modal_clan_create_btn = buttons[-1]
    # wait.until(lambda d: modal_clan_create_btn.is_enabled())
    # modal_clan_create_btn.click()
    # return clan_name


def delete_clan(driver, wait, clan_name):

    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))).click()
    clan_settings_menu = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']")
        )
    )
    clan_settings_menu[3].click()
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-settings-sidebar-delete']")
        )
    ).click()
    confirm_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-input']")
        )
    )
    confirm_input.send_keys(clan_name)
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-confirm']")
        )
    ).click()

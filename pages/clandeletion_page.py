from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class DeleteClanModal:
    CLAN_HEADER_TITLE = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"
    )
    CLAN_SETTINGS_MENU_ITEMS = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']"
    )
    SETTINGS_SIDEBAR_DELETE = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-settings-sidebar-delete']"
    )
    DELETE_CLAN_CONFIRM_INPUT = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-input']"
    )
    DELETE_CLAN_CONFIRM_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-settings-modal-delete_clan-confirm']"
    )

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open_clan_settings_menu(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CLAN_HEADER_TITLE)
        ).click()

    def click_settings_menu_item(self, index=3):
        menu_items = self.wait.until(
            EC.presence_of_all_elements_located(self.CLAN_SETTINGS_MENU_ITEMS)
        )
        menu_items[index].click()

    def click_settings_sidebar_delete(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SETTINGS_SIDEBAR_DELETE)
        ).click()

    def input_delete_clan_name(self, clan_name):
        confirm_input = self.wait.until(
            EC.presence_of_element_located(self.DELETE_CLAN_CONFIRM_INPUT)
        )
        confirm_input.send_keys(clan_name)

    def click_confirm_delete(self):
        self.wait.until(
            EC.element_to_be_clickable(self.DELETE_CLAN_CONFIRM_BUTTON)
        ).click()

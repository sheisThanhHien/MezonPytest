import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CreateCategoryModal:
    CLAN_HEADER_TITLE = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"
    )
    CLAN_SETTINGS_MENU_ITEMS = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']"
    )
    CREATE_CATEGORY_INPUT = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-input-category_name']"
    )
    CREATE_CATEGORY_CONFIRM_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-button-confirm']"
    )

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open_clan_settings_menu(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CLAN_HEADER_TITLE)
        ).click()

    def click_settings_menu_item(self, index):
        menu_items = self.wait.until(
            EC.presence_of_all_elements_located(self.CLAN_SETTINGS_MENU_ITEMS)
        )
        menu_items[index].click()

    def click_show_empty_categories(self):
        self.click_settings_menu_item(5)
        time.sleep(0.5)

    def click_create_category_option(self):
        self.click_settings_menu_item(0)

    def input_category_name(self, category_name):
        self.wait.until(
            EC.presence_of_element_located(self.CREATE_CATEGORY_INPUT)
        ).send_keys(category_name)

    def click_confirm_create_category(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_CATEGORY_CONFIRM_BUTTON)
        ).click()

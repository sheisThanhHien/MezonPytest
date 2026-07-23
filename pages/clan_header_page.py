import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ClanHeaderPage(BasePage):
    CLAN_HEADER_TITLE = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-header-title-clan_name']",
    )

    CREATE_CATEGORY_MENU_INDEX = 0
    MARK_AS_READ_MENU_INDEX = 1
    INVITE_PEOPLE_MENU_INDEX = 2
    CLAN_SETTINGS_MENU_INDEX = 3
    NOTIFICATIONS_SETTINGS_MENU_INDEX = 4
    SHOW_EMPTY_CATEGORIES_MENU_INDEX = 5

    CLAN_SETTINGS_MENU_ITEMS = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-header-modal_panel-item']",
    )

    def dismiss_backdrop(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def open_settings_menu(self):
        self.dismiss_backdrop()
        header = self.wait.until(
            EC.presence_of_element_located(self.CLAN_HEADER_TITLE)
        )
        self.js_click(header)

    def click_settings_menu_item(self, label):
        menu_items = self.wait.until(
            EC.presence_of_all_elements_located(self.CLAN_SETTINGS_MENU_ITEMS)
        )
        target_label = label.strip().lower()

        for item in menu_items:
            if target_label in item.text.strip().lower():
                item.click()
                return

        available = [item.text.strip() for item in menu_items if item.text.strip()]
        raise AssertionError(
            f"Settings menu item '{label}' not found. Available: {available}"
        )

    def click_settings_menu_item_by_index(self, index):
        menu_items = self.wait.until(
            EC.presence_of_all_elements_located(self.CLAN_SETTINGS_MENU_ITEMS)
        )

        if index < 0 or index >= len(menu_items):
            available = [
                item.text.strip() for item in menu_items if item.text.strip()
            ]
            raise AssertionError(
                f"Settings menu index {index} out of range. Available: {available}"
            )

        menu_items[index].click()

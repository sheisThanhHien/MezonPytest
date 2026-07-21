from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.clan_header_page import ClanHeaderPage


class DeleteClanPage(ClanHeaderPage):
    SETTINGS_MENU_LABEL = "Clan Settings"
    SETTINGS_SIDEBAR_DELETE = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-settings-sidebar-delete']",
    )
    DELETE_CLAN_CONFIRM_INPUT = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-settings-modal-delete_clan-input']",
    )
    DELETE_CLAN_CONFIRM_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-settings-modal-delete_clan-confirm']",
    )
    CLAN_LIST_ITEM = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-side_bar-clan_item']",
    )

    def open_clan_settings(self):
        self.open_settings_menu()
        self.click_settings_menu_item(self.SETTINGS_MENU_LABEL)

    def click_settings_sidebar_delete(self):
        delete_button = self.wait.until(
            EC.presence_of_element_located(self.SETTINGS_SIDEBAR_DELETE)
        )
        self.js_click(delete_button)

    def input_delete_clan_name(self, clan_name):
        confirm_input = self.wait.until(
            EC.presence_of_element_located(self.DELETE_CLAN_CONFIRM_INPUT)
        )
        confirm_input.send_keys(clan_name)

    def click_confirm_delete(self):
        self.wait.until(
            EC.element_to_be_clickable(self.DELETE_CLAN_CONFIRM_BUTTON)
        ).click()

    def delete_clan(self, clan_name):
        self.open_clan_settings()
        self.click_settings_sidebar_delete()
        self.input_delete_clan_name(clan_name)
        self.click_confirm_delete()

    def verify_clan_deleted(self, clan_name):
        target_name = clan_name.strip().upper()

        def clan_removed():
            for item in self.driver.find_elements(*self.CLAN_LIST_ITEM):
                try:
                    if target_name in item.text.strip().upper():
                        return False
                except StaleElementReferenceException:
                    continue
            return clan_name

        return self.poll_until(
            clan_removed,
            f"Clan '{clan_name}' still exists in sidebar after deletion.",
        )


# Backward-compatible alias
DeleteClanModal = DeleteClanPage

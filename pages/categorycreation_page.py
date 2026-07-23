from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.clan_header_page import ClanHeaderPage


class CreateCategoryPage(ClanHeaderPage):
    CREATE_CATEGORY_INPUT = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-modal-create_category-input-category_name']",
    )
    CREATE_CATEGORY_CONFIRM_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-modal-create_category-button-confirm']",
    )
    CATEGORY_NAME = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-side_bar-channel_list-category-name']",
    )

    def click_create_category_option(self):
        self.open_settings_menu()
        self.click_settings_menu_item_by_index(ClanHeaderPage.CREATE_CATEGORY_MENU_INDEX) 

    def input_category_name(self, category_name):
        self.wait.until(
            EC.presence_of_element_located(self.CREATE_CATEGORY_INPUT)
        ).send_keys(category_name)

    def click_confirm_create_category(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_CATEGORY_CONFIRM_BUTTON)
        ).click()

    def verify_category_created(self, category_name):
        def category_exists(driver):
            categories = driver.find_elements(*self.CATEGORY_NAME)
            for category in categories:
                if category.text.strip().upper() == category_name.upper():
                    return True
            return False

        return self.wait.until(category_exists)


# Backward-compatible alias
CreateCategoryModal = CreateCategoryPage

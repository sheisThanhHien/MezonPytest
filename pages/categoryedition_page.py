import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class EditCategoryModal:
    CATEGORY_CONTAINER = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']"
    )
    CATEGORY_NAME = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category-name']"
    )
    EDIT_OPTION = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-panel-item']"
    )
    EDIT_CATEGORY_INPUT = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-edit_category-input-name']"
    )
    EDIT_CATEGORY_CONFIRM_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-edit_category-button-confirm']"
    )

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def find_category_container(self, category_name):
        category_containers = self.wait.until(
            EC.presence_of_all_elements_located(self.CATEGORY_CONTAINER)
        )
        target_name = category_name.upper()

        for container in category_containers:
            try:
                name_element = container.find_element(*self.CATEGORY_NAME)
                if target_name in name_element.text.strip().upper():
                    return container
            except StaleElementReferenceException:
                continue

        return None

    def open_edit_menu(self, category_name):
        target_container = self.find_category_container(category_name)
        assert target_container is not None, f"Cannot find category '{category_name}'"

        ActionChains(self.driver).context_click(target_container).perform()
        time.sleep(0.5)

        self.wait.until(
            EC.element_to_be_clickable(self.EDIT_OPTION)
        ).click()

    def input_category_name(self, category_name):
        edit_input = self.wait.until(
            EC.presence_of_element_located(self.EDIT_CATEGORY_INPUT)
        )
        edit_input.clear()
        edit_input.send_keys(category_name)

    def click_confirm_edit_category(self):
        self.wait.until(
            EC.element_to_be_clickable(self.EDIT_CATEGORY_CONFIRM_BUTTON)
        ).click()

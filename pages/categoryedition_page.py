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
    EDIT_CATEGORY_OPTION = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-panel-item']"
    )
    EDIT_CATEGORY_INPUT = (
        By.CLASS_NAME, "text-theme-primary-active outline-none w-full h-10 p-[10px] bg-theme-input border-theme-primary text-base rounded placeholder:text-sm"
    )
    EDIT_CATEGORY_SAVECHANGES_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-edit_category-button-confirm']"
    )

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def find_category_container(self, category_name):
    # Get all category containers in left sidebar
        category_containers = self.wait.until(
            EC.presence_of_all_elements_located(self.CATEGORY_CONTAINER)
        )

        target_name = category_name.upper()

        # Find the category container that matches category_name
        for container in category_containers:
            try:
                name_element = container.find_element(*self.CATEGORY_NAME)
                actual_name = name_element.text.strip().upper()

                if target_name in actual_name:
                    return container

            except StaleElementReferenceException:
                continue

        raise AssertionError(f"Cannot find category '{category_name}'")


    def open_edit_menu(self, category_name):
        # Right-click on target category
        target_container = self.find_category_container(category_name)
        ActionChains(self.driver).context_click(target_container).perform()


    def click_edit_category_option(self):
        # Index 5 = Edit Category option
        menu_items = self.wait.until(
            EC.presence_of_all_elements_located(self.EDIT_CATEGORY_OPTION)
        )

        menu_items[5].click()


    def input_category_name(self, category_name):
        # Clear old category name and input new category name
        edit_input = self.wait.until(
            EC.visibility_of_element_located(self.EDIT_CATEGORY_INPUT)
        )

        edit_input.clear()
        edit_input.send_keys(category_name)


    def click_save_changes_button(self):
        # Click Save Changes button
        self.wait.until(
            EC.element_to_be_clickable(self.EDIT_CATEGORY_SAVECHANGES_BUTTON)
        ).click()

    # def find_category_container(self, category_name):
    #     category_containers = self.wait.until(
    #         EC.presence_of_all_elements_located(self.CATEGORY_CONTAINER)
    #     )
    #     target_name = category_name.upper()

    #     for container in category_containers:
    #         try:
    #             name_element = container.find_element(*self.CATEGORY_NAME)
    #             if target_name in name_element.text.strip().upper():
    #                 return container
    #         except StaleElementReferenceException:
    #             continue

    #     return None

    # def open_edit_menu(self, category_name):
    #     target_container = self.find_category_container(category_name)
    #     assert target_container is not None, f"Cannot find category '{category_name}'"

    #     ActionChains(self.driver).context_click(target_container).perform()
    #     time.sleep(0.5)

    #     self.wait.until(
    #         EC.element_to_be_clickable(self.EDIT_CATEGORY_OPTION)
    #     ).click()

    # def input_category_name(self, category_name):
    #     edit_input = self.wait.until(
    #         EC.presence_of_element_located(self.EDIT_CATEGORY_INPUT)
    #     )
    #     edit_input.clear()
    #     edit_input.send_keys(category_name)

    # def click_save_changes_button(self):
    #     self.wait.until(
    #         EC.element_to_be_clickable(self.EDIT_CATEGORY_SAVECHANGES_BUTTON)
    #     ).click()

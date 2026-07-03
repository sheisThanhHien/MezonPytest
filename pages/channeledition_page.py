from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class ChannelEditionPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    CHANNEL_LIST_ITEM = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']"
    )
    CHANNEL_LIST_ITEM_NAME = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item-name']"
    )
    EDIT_CHANNEL_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-panel-item']"
    )
    # EDIT_CHANNEL_INPUT = (
    #     By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item-input']"
    # )
    EDIT_CHANNEL_SAVECHANGES_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='button-base']"
    )
    SIDEBAR_CHANNEL_LABEL = (
        By.CSS_SELECTOR, "[data-e2e='channel_setting_page-side_bar-channel_label']"
    )

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def find_channel_container(self, channel_name):
        channel_containers = self.wait.until(
            EC.presence_of_all_elements_located(self.CHANNEL_LIST_ITEM)
        )
        target_name = channel_name.upper()
        for container in channel_containers:
            try:
                name_element = container.find_element(*self.CHANNEL_LIST_ITEM_NAME)
                actual_name = name_element.text.strip().upper()
                if actual_name == target_name:
                    return container
            except StaleElementReferenceException:
                continue
        raise AssertionError(f"Cannot find channel '{channel_name}'")

    def open_channel_context_menu(self, channel_name):
        target_container = self.find_channel_container(channel_name)
        ActionChains(self.driver).context_click(target_container).perform()

    def click_edit_channel_option(self):  
        menu_option = self.wait.until(
            EC.element_to_be_clickable(self.EDIT_CHANNEL_BUTTON)
        )
        menu_option[5].click()

    def input_channel_name(self, channel_name):
        edit_input = self.wait.until(
            EC.visibility_of_element_located(self.EDIT_CHANNEL_INPUT)
        )
        edit_input.clear()
        edit_input.send_keys(channel_name)

    def click_save_changes_button(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.EDIT_CHANNEL_SAVECHANGES_BUTTON)
        )
        buttons[1].click()

    def verify_sidebar_new_channel_name(self, channel_name):
        target_container = self.find_channel_container(channel_name)
        name_element = target_container.find_element(*self.SIDEBAR_CHANNEL_LABEL)
        actual_name = name_element.text.strip().upper()
        assert actual_name == channel_name.upper(), f"Sidebar channel name is not '{channel_name}'"
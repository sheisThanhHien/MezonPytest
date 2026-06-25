from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ChannelPage:
    # Locators
    CATEGORY_CONTAINER = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']"
    )
    CATEGORY_NAME = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category-name']"
    )
    CREATE_CHANNEL_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-button-add_channel']"
    )
    CHANNEL_TYPE = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_channel-type']"
    )
    MODAL_CHANNEL_NAME_INPUT = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_channel-input-channel_name']"
    )
    PRIVATE_CHANNEL_TOGGLE = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_channel-toggle-is_private']"
    )
    CREATE_CHANNEL_BUTTON_BASE = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_channel-button-confirm']"
    )

    CHANNEL_LIST_ITEM = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']"
    )
    CHANNEL_LIST_ITEM_NAME = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item-name']"
    )

    # CONSTRUCTORS
    def __init__ (self, driver, wait):
        self.driver = driver
        self.wait = wait

    # ACTIONS
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

        raise AssertionError(f"Cannot find category '{category_name}'")

    def get_channel_items_in_category(self, category_name):
        container = self.find_category_container(category_name)
        wrapper = container.find_element(By.XPATH, "..")
        channels = []

        for sibling in wrapper.find_elements(By.XPATH, "./following-sibling::*"):
            e2e = sibling.get_attribute("data-e2e") or ""
            if e2e == "clan_page-channel_list-item":
                channels.append(sibling)
            elif e2e == "clan_page-side_bar-channel_list-category":
                break
            elif sibling.find_elements(*self.CATEGORY_CONTAINER):
                break

        return channels

    def _matches_channel_name(self, expected, actual):
        expected = expected.strip().upper()
        actual = actual.strip().upper().replace("...", "").rstrip(".")
        if not actual:
            return False
        return expected.startswith(actual) or actual in expected

    def click_create_channel_button(self, category_name=None):
        if category_name:
            container = self.find_category_container(category_name)
            container.find_element(*self.CREATE_CHANNEL_BUTTON).click()
            return

        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_CHANNEL_BUTTON)
        ).click()

    def click_text_channel_type(self):
        channel_types = self.wait.until(EC.presence_of_all_elements_located(self.CHANNEL_TYPE))
        channel_types[0].click()

    def click_voice_channel_type(self):
        channel_types = self.wait.until(EC.presence_of_all_elements_located(self.CHANNEL_TYPE))
        channel_types[1].click()

    def click_stream_channel_type(self):
        channel_types = self.wait.until(EC.presence_of_all_elements_located(self.CHANNEL_TYPE))
        channel_types[2].click()

    def input_channel_name(self, channel_name):
        self.wait.until(
            EC.presence_of_element_located(self.MODAL_CHANNEL_NAME_INPUT)
        ).send_keys(channel_name)

    def click_confirm_create_channel(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_CHANNEL_BUTTON_BASE)
        ).click()


    def verify_channel_created(self, channel_name, category_name=None):
        if category_name:
            def channel_in_category(driver):
                try:
                    for item in self.get_channel_items_in_category(category_name):
                        name_elements = item.find_elements(*self.CHANNEL_LIST_ITEM_NAME)
                        texts = [el.text for el in name_elements] if name_elements else [item.text]
                        if any(self._matches_channel_name(channel_name, text) for text in texts):
                            return True
                except (StaleElementReferenceException, AssertionError):
                    pass
                return False

            return self.wait.until(channel_in_category)

        def channel_found(driver):
            try:
                for item in driver.find_elements(*self.CHANNEL_LIST_ITEM):
                    name_elements = item.find_elements(*self.CHANNEL_LIST_ITEM_NAME)
                    texts = [el.text for el in name_elements] if name_elements else [item.text]
                    if any(self._matches_channel_name(channel_name, text) for text in texts):
                        return True
            except StaleElementReferenceException:
                pass
            return False

        return self.wait.until(channel_found)

    def open_channel(self, channel_name):
        def channel_clickable(driver):
            try:
                for item in driver.find_elements(*self.CHANNEL_LIST_ITEM):
                    name_elements = item.find_elements(*self.CHANNEL_LIST_ITEM_NAME)
                    texts = [el.text for el in name_elements] if name_elements else [item.text]
                    if any(self._matches_channel_name(channel_name, text) for text in texts):
                        item.click()
                        return True
            except StaleElementReferenceException:
                pass
            return False

        self.wait.until(channel_clickable)


from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ChannelPage:
    # Locators
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
    def click_create_channel_button(self):
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




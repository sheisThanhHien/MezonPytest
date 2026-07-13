import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.message_page import MessagePage


class MessagePinPage(MessagePage):
    PIN_CONFIRM_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-message_action_modal-confirm_modal-button-confirm']",
    )
    PIN_SYSTEM_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-system_message']",
    )
    PIN_SYSTEM_MESSAGE_CONTENT = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-system_message-7']",
    )
    PIN_SYSTEM_MESSAGE_SEE_ALL_PINNED = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-system_message-pin_message-button-see_all_pinned']",
    )
    PIN_SYSTEM_MESSAGE_JUMP = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-system_message-pin_message-button-jump_to_message']",
    )
    PIN_LIST_ITEM = (By.CSS_SELECTOR, "[data-e2e='common-pin_message']")
    PIN_MENU_ICON_PATH = "M19.38 11.38"

    def _confirm_pin_message(self):
        confirm_button = self.wait.until(
            EC.element_to_be_clickable(self.PIN_CONFIRM_BUTTON)
        )
        confirm_button.click()

    def pin_message(self, message):
        message_item = self._find_message_item_by_text(message)
        self._open_context_menu(message_item)
        self._click_context_menu_item(self.PIN_MENU_ICON_PATH)
        self._confirm_pin_message()
        return message_item

    def _verify_pin_system_message(self):
        self.wait.until(EC.visibility_of_element_located(self.PIN_SYSTEM_MESSAGE))
        self.wait.until(
            EC.visibility_of_element_located(self.PIN_SYSTEM_MESSAGE_CONTENT)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.PIN_SYSTEM_MESSAGE_SEE_ALL_PINNED)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.PIN_SYSTEM_MESSAGE_JUMP)
        )

    def _open_pin_list(self):
        see_all_button = self.wait.until(
            EC.element_to_be_clickable(self.PIN_SYSTEM_MESSAGE_SEE_ALL_PINNED)
        )
        see_all_button.click()

    def _verify_message_in_pin_list(self, message):
        deadline = time.time() + 120

        while time.time() < deadline:
            for item in self.driver.find_elements(*self.PIN_LIST_ITEM):
                if item.is_displayed() and message in item.text:
                    return message

            time.sleep(1)

        raise AssertionError(
            f"Could not find pinned message '{message}' in pin list."
        )

    def verify_message_pinned(self, message):
        self._verify_pin_system_message()
        self._open_pin_list()
        self._verify_message_in_pin_list(message)

        return message

import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pages.message_page import MessagePage


class MessageEditPage(MessagePage):
    INLINE_EDITOR = (By.CSS_SELECTOR, ".mention-input-editor")
    EDIT_MENU_ICON_PATH = "m13.96 5.46"

    def click_edit_message(self, message):
        item = self._find_message_item_by_text(message)
        self._open_context_menu(item)
        self._click_context_menu_item(self.EDIT_MENU_ICON_PATH)
        return item

    def _find_inline_editor_in_message(self, message_item):
        editors = message_item.find_elements(*self.INLINE_EDITOR)
        for editor in editors:
            if editor.is_displayed():
                return editor
        return None

    def submit_inline_edit(self, new_message, message_item):
        editor = self.wait.until(
            lambda driver: self._find_inline_editor_in_message(message_item)
        )
        editor.click()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        editor.send_keys(new_message)
        editor.send_keys(Keys.ENTER)

    def edit_message(self, original_message, new_message):
        message_item = self.click_edit_message(original_message)
        self.submit_inline_edit(new_message, message_item)

    def verify_message_text(self, message):
        deadline = time.time() + 120

        while time.time() < deadline:
            for item in reversed(self.driver.find_elements(*self.MESSAGE_ITEM)):
                try:
                    if self._get_message_text(item) != message:
                        continue

                    item_class = item.get_attribute("class") or ""
                    text_nodes = item.find_elements(*self.MESSAGE_TEXT)
                    text_class = text_nodes[0].get_attribute("class") or ""
                    if "is-error" in item_class:
                        raise AssertionError(f"Message edit failed: {message}")
                    if (
                        "pointer-events-none" not in item_class
                        and "opacity-50" not in text_class
                    ):
                        return message
                except StaleElementReferenceException:
                    continue

            time.sleep(1)

        raise AssertionError(f"Could not find message with text '{message}'.")

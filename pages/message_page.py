import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MessagePage:
    CHAT_INPUT = (By.CSS_SELECTOR, "[data-e2e='mention-input']")
    MESSAGE_ITEM = (By.CSS_SELECTOR, "[data-e2e='message-item']")
    MESSAGE_TEXT = (By.XPATH, ".//div[contains(@class,'text-theme-message')]")
    CONTEXT_MENU_ITEM = (By.CSS_SELECTOR, "[role='menuitem']")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def _normalize_message_text(self, text):
        return text.replace("(edited)", "").strip()

    def _get_message_text(self, item):
        text_nodes = item.find_elements(*self.MESSAGE_TEXT)
        if not text_nodes:
            return ""
        return self._normalize_message_text(text_nodes[0].text)

    def _find_message_item_by_text(self, message):
        deadline = time.time() + 120

        while time.time() < deadline:
            for item in reversed(self.driver.find_elements(*self.MESSAGE_ITEM)):
                try:
                    if self._get_message_text(item) == message:
                        return item
                except StaleElementReferenceException:
                    continue

            time.sleep(1)

        raise AssertionError(f"Could not find message '{message}'.")

    def _open_context_menu(self, item):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", item
        )
        ActionChains(self.driver).context_click(item).perform()

    def _get_visible_context_menu_items(self):
        return [
            item
            for item in self.driver.find_elements(*self.CONTEXT_MENU_ITEM)
            if item.is_displayed()
        ]

    def send_message(self, message):
        chat_input = self.wait.until(
            EC.presence_of_element_located(self.CHAT_INPUT)
        )
        chat_input.send_keys(message)
        chat_input.send_keys(Keys.ENTER)

    def verify_message_sent(self, message):
        deadline = time.time() + 120

        while time.time() < deadline:
            for item in reversed(self.driver.find_elements(*self.MESSAGE_ITEM)):
                try:
                    text_nodes = item.find_elements(*self.MESSAGE_TEXT)
                    if not text_nodes or text_nodes[0].text.strip() != message:
                        continue

                    item_class = item.get_attribute("class") or ""
                    text_class = text_nodes[0].get_attribute("class") or ""
                    if "is-error" in item_class:
                        raise AssertionError(f"Message send failed: {message}")
                    if (
                        "pointer-events-none" not in item_class
                        and "opacity-50" not in text_class
                    ):
                        return message
                except StaleElementReferenceException:
                    continue

            time.sleep(1)

        raise AssertionError(f"Could not find sent message '{message}'.")

        #EDIT MESSAGES 

    def click_edit_message(self, message):
        item = self._find_message_item_by_text(message)
        self._open_context_menu(item)

        def menu_has_edit_option(driver):
            return len(self._get_visible_context_menu_items()) >= 2

        self.wait.until(menu_has_edit_option)

        menu_items = self._get_visible_context_menu_items()
        edit_item = menu_items[1]
        if edit_item.text.strip() != "Edit Message":
            raise AssertionError(
                "Expected 'Edit Message' at menu position 2, "
                f"got '{edit_item.text.strip()}'"
            )
        edit_item.click()
        return item

    def _find_inline_editor_in_message(self, message_item):
        editors = message_item.find_elements(By.CSS_SELECTOR, ".mention-input-editor")
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

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
    CONTEXT_MENU = (By.CSS_SELECTOR, "div.contexify[role='menu']")

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

    def _get_visible_context_menu(self):
        for menu in self.driver.find_elements(*self.CONTEXT_MENU):
            if menu.is_displayed():
                return menu
        return None

    def _click_context_menu_item(self, icon_path_fragment):
        menu_item_xpath = (
            ".//div[@role='menuitem' and contains(@class,'contexify_item')]"
        )

        def item_visible(driver):
            menu = self._get_visible_context_menu()
            if menu is None:
                return False

            for item in menu.find_elements(By.XPATH, menu_item_xpath):
                if not item.is_displayed():
                    continue
                try:
                    path_d = item.find_element(
                        By.CSS_SELECTOR, "svg path"
                    ).get_attribute("d")
                except Exception:
                    continue
                if path_d and icon_path_fragment in path_d:
                    return item
            return False

        item = self.wait.until(item_visible)
        item.click()

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
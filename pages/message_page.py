import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MessagePage:
    CHAT_INPUT = (By.CSS_SELECTOR, "[data-e2e='mention-input']")
    MESSAGE_ITEM = (By.CSS_SELECTOR, "[data-e2e='message-item']")
    MESSAGE_TEXT = (By.XPATH, ".//div[contains(@class,'text-theme-message')]")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

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

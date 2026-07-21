import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.message_page import MessagePage


class ThreadBasePage(MessagePage):
    THREAD_NAME_INPUT = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-thread_box-input-thread_name']",
    )
    THREAD_DISCUSSION_BOX = (By.CSS_SELECTOR, "[data-e2e='discussion-box-thread']")
    THREAD_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='discussion-header-button-close']",
    )
    THREAD_SYSTEM_MESSAGE = (By.CSS_SELECTOR, "[data-e2e='chat-system_message']")
    THREAD_SIDEBAR_ITEM_NAME = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-channel_list-thread_item-name']",
    )
    TOPIC_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-topic-header-button-close']",
    )
    THREAD_LIST_ITEM = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread-item']",
    )
    CHANNEL_LIST_ITEM = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-channel_list-item']",
    )

    def _thread_name_matches(self, thread_name, actual_text):
        expected = thread_name.strip()
        actual = " ".join(actual_text.split())
        if not actual:
            return False
        if expected in actual:
            return True

        shortened = actual.replace("...", "").rstrip(".")
        return expected.startswith(shortened) or shortened in expected

    def dismiss_overlays(self):
        for close_button in self.driver.find_elements(*self.TOPIC_CLOSE_BUTTON):
            if close_button.is_displayed():
                self.js_click(close_button)
                break

        for close_button in self.driver.find_elements(*self.THREAD_CLOSE_BUTTON):
            if close_button.is_displayed():
                self.js_click(close_button)
                break

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def ensure_channel_view(self):
        for channel_item in self.driver.find_elements(*self.CHANNEL_LIST_ITEM):
            if channel_item.is_displayed():
                self.js_click(channel_item)
                time.sleep(0.5)
                return

    def input_thread_name(self, thread_name):
        thread_name_input = self.wait.until(
            EC.visibility_of_element_located(self.THREAD_NAME_INPUT)
        )
        thread_name_input.click()
        thread_name_input.send_keys(Keys.CONTROL, "a")
        thread_name_input.send_keys(Keys.BACKSPACE)
        thread_name_input.send_keys(thread_name)

    def send_starter_message(self, starter_message):
        thread_box = self.wait.until(
            EC.visibility_of_element_located(self.THREAD_DISCUSSION_BOX)
        )
        chat_input = thread_box.find_element(*self.CHAT_INPUT)
        chat_input.click()
        chat_input.send_keys(starter_message)
        chat_input.send_keys(Keys.ENTER)

    def close_thread_panel(self):
        for close_button in self.driver.find_elements(*self.THREAD_CLOSE_BUTTON):
            if close_button.is_displayed():
                self.js_click(close_button)
                return

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def close_thread_list(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def close_thread(self):
        self.close_thread_panel()

    def verify_thread_in_sidebar(self, thread_name):
        def thread_found():
            for item in self.driver.find_elements(*self.THREAD_SIDEBAR_ITEM_NAME):
                try:
                    if item.is_displayed() and self._thread_name_matches(
                        thread_name, item.text
                    ):
                        return thread_name
                except StaleElementReferenceException:
                    continue
            return None

        return self.poll_until(
            thread_found,
            f"Could not find thread '{thread_name}' in channel sidebar.",
        )

    def verify_thread_created_system_message(self, thread_name):
        def system_message_found():
            messages = [
                message
                for message in self.driver.find_elements(*self.THREAD_SYSTEM_MESSAGE)
                if message.is_displayed()
            ]

            for message in reversed(messages):
                text = message.text
                if "started a thread" in text.lower() and self._thread_name_matches(
                    thread_name, text
                ):
                    return message
            return None

        return self.poll_until(
            system_message_found,
            f"System message does not contain thread name '{thread_name}'.",
        )

    def verify_starter_message_in_thread(self, starter_message):
        def starter_found():
            thread_boxes = [
                box
                for box in self.driver.find_elements(*self.THREAD_DISCUSSION_BOX)
                if box.is_displayed()
            ]

            for container in thread_boxes:
                for item in container.find_elements(*self.MESSAGE_ITEM):
                    if self._get_message_text(item) == starter_message:
                        return starter_message

            for item in reversed(self.driver.find_elements(*self.MESSAGE_ITEM)):
                try:
                    if item.is_displayed() and self._get_message_text(item) == starter_message:
                        return starter_message
                except StaleElementReferenceException:
                    continue
            return None

        return self.poll_until(
            starter_found,
            f"Could not find starter message '{starter_message}' in thread.",
        )

    def verify_source_message_in_thread(self, source_message):
        def source_found():
            thread_boxes = [
                box
                for box in self.driver.find_elements(*self.THREAD_DISCUSSION_BOX)
                if box.is_displayed()
            ]

            for container in thread_boxes:
                if source_message in container.text:
                    return source_message
            return None

        return self.poll_until(
            source_found,
            f"Could not find source message '{source_message}' in thread.",
        )

    def jump_to_thread_from_system_message(self, thread_name):
        system_message = self.verify_thread_created_system_message(thread_name)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", system_message
        )

        thread_link = system_message.find_element(
            By.XPATH, f".//span[contains(text(), '{thread_name}')]"
        )
        ActionChains(self.driver).move_to_element(thread_link).click().perform()

    def verify_jump_to_thread(self, thread_name, starter_message):
        def thread_view_open(driver):
            sidebar_item = None
            for item in driver.find_elements(*self.THREAD_SIDEBAR_ITEM_NAME):
                if item.is_displayed() and self._thread_name_matches(
                    thread_name, item.text
                ):
                    sidebar_item = item
                    break

            if sidebar_item is None:
                return False

            sidebar_row = sidebar_item.find_element(By.XPATH, "../..")
            sidebar_class = sidebar_row.get_attribute("class") or ""
            return "text-theme-primary-active" in sidebar_class

        self.wait.until(thread_view_open)
        self.verify_starter_message_in_thread(starter_message)
        return thread_name

    @staticmethod
    def validate_thread_name(thread_name):
        if len(thread_name.strip()) <= 3:
            raise ValueError("Thread name must be longer than 3 characters.")

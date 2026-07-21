import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.thread_base_page import ThreadBasePage


class ThreadListPage(ThreadBasePage):
    THREADS_HEADER_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread']",
    )
    CREATE_THREAD_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread-modal-thread_management-button-create_thread']",
    )
    THREAD_CREATED_SYSTEM_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-system_message-6']",
    )

    def open_thread_list(self):
        self.dismiss_overlays()
        self.ensure_channel_view()
        header = self.wait.until(
            EC.presence_of_element_located(self.THREADS_HEADER_BUTTON)
        )
        button = header.find_element(By.TAG_NAME, "button")

        deadline = time.time() + 30
        while time.time() < deadline:
            self.js_click(button)
            time.sleep(0.5)

            if any(
                element.is_displayed()
                for element in self.driver.find_elements(*self.CREATE_THREAD_BUTTON)
            ):
                return

            if any(
                element.is_displayed()
                for element in self.driver.find_elements(
                    By.CSS_SELECTOR, "[data-e2e*='thread_management']"
                )
            ):
                return

            if any(
                element.is_displayed()
                for element in self.driver.find_elements(*self.THREAD_LIST_ITEM)
            ):
                return

        raise AssertionError("Could not open thread list panel.")

    def click_create_thread(self):
        create_button = self.wait.until(
            EC.presence_of_element_located(self.CREATE_THREAD_BUTTON)
        )
        self.js_click(create_button)

    def create_public_thread(self, thread_name, starter_message):
        self.validate_thread_name(thread_name)
        self.open_thread_list()
        self.click_create_thread()
        self.input_thread_name(thread_name)
        self.send_starter_message(starter_message)
        self.wait.until(
            EC.visibility_of_element_located(self.THREAD_CREATED_SYSTEM_MESSAGE)
        )

        return thread_name, starter_message

    def verify_thread_in_thread_list(self, thread_name, starter_message=None):
        self.open_thread_list()

        def thread_in_list(driver):
            try:
                for item in driver.find_elements(*self.THREAD_LIST_ITEM):
                    if not item.is_displayed():
                        continue

                    item_text = item.text
                    if not self._thread_name_matches(thread_name, item_text):
                        continue

                    if starter_message and starter_message not in item_text:
                        continue

                    return True
            except StaleElementReferenceException:
                pass
            return False

        self.wait.until(thread_in_list)
        self.close_thread_list()
        return thread_name

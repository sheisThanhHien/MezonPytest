import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.message_page import MessagePage


class ThreadPage(MessagePage):
    THREADS_HEADER_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread']",
    )
    CREATE_THREAD_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread-modal-thread_management-button-create_thread']",
    )
    THREAD_NAME_INPUT = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-thread_box-input-thread_name']",
    )
    THREAD_DISCUSSION_BOX = (By.CSS_SELECTOR, "[data-e2e='discussion-box-thread']")
    THREAD_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='discussion-header-button-close']",
    )
    THREAD_CREATED_SYSTEM_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-system_message-6']",
    )
    THREAD_SIDEBAR_ITEM_NAME = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-channel_list-thread_item-name']",
    )
    THREAD_LIST_ITEM = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread-item']",
    )

    def open_thread_list(self):
        thread_button = self.wait.until(
            EC.element_to_be_clickable(self.THREADS_HEADER_BUTTON)
            )
        thread_button.click()

    def click_create_thread(self):
        create_button = self.wait.until(
            EC.element_to_be_clickable(self.CREATE_THREAD_BUTTON)
        )
        create_button.click()

    def input_thread_name(self, thread_name):
        thread_name_input = self.wait.until(
            EC.visibility_of_element_located(self.THREAD_NAME_INPUT)
        )
        thread_name_input.clear()
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
        close_button = self.wait.until(
            EC.element_to_be_clickable(self.THREAD_CLOSE_BUTTON)
        )
        close_button.click()

    def _find_visible_thread_sidebar_item(self, thread_name):
        deadline = time.time() + 120

        while time.time() < deadline:
            for item in self.driver.find_elements(*self.THREAD_SIDEBAR_ITEM_NAME):
                try:
                    if item.is_displayed() and thread_name in item.text:
                        return item
                except StaleElementReferenceException:
                    continue

            time.sleep(1)

        raise AssertionError(
            f"Could not find thread '{thread_name}' in channel sidebar."
        )

    def verify_thread_in_sidebar(self, thread_name):
        self._find_visible_thread_sidebar_item(thread_name)
        return thread_name

    def close_thread_list(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()




    def verify_thread_in_thread_list(self, thread_name, starter_message=None):
        self.open_thread_list()

        def thread_in_list(driver):
            try:
                for item in driver.find_elements(*self.THREAD_LIST_ITEM):
                    if not item.is_displayed():
                        continue

                    item_text = item.text
                    if thread_name not in item_text:
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

    def verify_thread_created_system_message(self, thread_name):
        system_message = self.wait.until(
            EC.visibility_of_element_located(self.THREAD_CREATED_SYSTEM_MESSAGE)
        )

        if thread_name not in system_message.text:
            raise AssertionError(
                f"System message does not contain thread name '{thread_name}'."
            )

        return system_message

    def verify_starter_message_in_thread(self, starter_message):
        deadline = time.time() + 120

        while time.time() < deadline:
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

            time.sleep(1)

        raise AssertionError(
            f"Could not find starter message '{starter_message}' in thread."
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
                if item.is_displayed() and thread_name in item.text:
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

    def create_public_thread(self, thread_name, starter_message):
        if len(thread_name.strip()) <= 3:
            raise ValueError("Thread name must be longer than 3 characters.")

        self.open_thread_list()
        self.click_create_thread()
        self.input_thread_name(thread_name)
        self.send_starter_message(starter_message)
        self.wait.until(
            EC.visibility_of_element_located(self.THREAD_CREATED_SYSTEM_MESSAGE)
        )

        return thread_name, starter_message

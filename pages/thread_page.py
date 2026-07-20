import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.message_page import MessagePage


class ThreadPage(MessagePage):
    # =========================================================================
    # LOCATORS
    # =========================================================================

    # --- Shared ---
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
    THREAD_SYSTEM_MESSAGE = (By.CSS_SELECTOR, "[data-e2e='chat-system_message']")
    THREAD_SIDEBAR_ITEM_NAME = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-channel_list-thread_item-name']",
    )
    TOPIC_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-topic-header-button-close']",
    )

    # --- Create thread from message ---
    CREATE_THREAD_MENU_LABEL = "Create Thread"
    CREATE_THREAD_HOVER_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-hover_message_actions-button-base']",
    )

    # --- Create public thread from thread list ---
    THREADS_HEADER_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread']",
    )
    CREATE_THREAD_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread-modal-thread_management-button-create_thread']",
    )
    THREAD_LIST_ITEM = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-channel_message-header-button-thread-item']",
    )

    # =========================================================================
    # COMMON
    # =========================================================================

    def _js_click(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)

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
                self._js_click(close_button)
                break

        for close_button in self.driver.find_elements(*self.THREAD_CLOSE_BUTTON):
            if close_button.is_displayed():
                self._js_click(close_button)
                break

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def ensure_channel_view(self):
        for channel_item in self.driver.find_elements(
            By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']"
        ):
            if channel_item.is_displayed():
                self._js_click(channel_item)
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
                self._js_click(close_button)
                return

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def close_thread_list(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def close_thread(self):
        self.close_thread_panel()

    def _find_visible_thread_sidebar_item(self, thread_name):
        deadline = time.time() + 120

        while time.time() < deadline:
            for item in self.driver.find_elements(*self.THREAD_SIDEBAR_ITEM_NAME):
                try:
                    if item.is_displayed() and self._thread_name_matches(
                        thread_name, item.text
                    ):
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

    def verify_thread_created_system_message(self, thread_name):
        deadline = time.time() + 120

        while time.time() < deadline:
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

            time.sleep(1)

        raise AssertionError(
            f"System message does not contain thread name '{thread_name}'."
        )

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

    # =========================================================================
    # CREATE THREAD FROM MESSAGE
    # =========================================================================

    def _click_create_thread_menu_item(self):
        def item_visible(driver):
            menu = self._get_visible_context_menu()
            if menu is None:
                return False

            try:
                item = menu.find_element(
                    By.XPATH,
                    ".//div[@role='menuitem'][contains(., 'Create Thread')]",
                )
                return item if item.is_displayed() else False
            except StaleElementReferenceException:
                return False

        self.wait.until(item_visible).click()

    def _click_create_thread_hover_button(self, source_message):
        message_item = self._find_message_item_by_text(source_message)
        ActionChains(self.driver).move_to_element(message_item).perform()
        time.sleep(0.5)

        def hover_button_visible(driver):
            current_item = self._find_message_item_by_text(source_message)
            for button in current_item.find_elements(*self.CREATE_THREAD_HOVER_BUTTON):
                if button.is_displayed() and button.get_attribute("title") == "Create Thread":
                    return button
            return False

        button = self.wait.until(hover_button_visible)
        ActionChains(self.driver).move_to_element(button).click(button).perform()

    def open_create_thread_panel_from_message(self, source_message):
        message_item = self._find_message_item_by_text(source_message)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", message_item
        )
        time.sleep(0.5)

        try:
            self._open_context_menu(message_item)
            self.wait.until(lambda driver: self._get_visible_context_menu() is not None)
            self._click_create_thread_menu_item()
        except TimeoutException:
            self._click_create_thread_hover_button(source_message)

        self.wait.until(EC.visibility_of_element_located(self.THREAD_DISCUSSION_BOX))
        return message_item

    def verify_source_message_in_thread(self, source_message):
        deadline = time.time() + 120

        while time.time() < deadline:
            thread_boxes = [
                box
                for box in self.driver.find_elements(*self.THREAD_DISCUSSION_BOX)
                if box.is_displayed()
            ]

            for container in thread_boxes:
                if source_message in container.text:
                    return source_message

            time.sleep(1)

        raise AssertionError(
            f"Could not find source message '{source_message}' in thread."
        )

    def create_thread_from_message(self, source_message, thread_name, starter_message):
        if len(thread_name.strip()) <= 3:
            raise ValueError("Thread name must be longer than 3 characters.")

        if not starter_message.strip():
            raise ValueError("Starter message is required.")

        self.open_create_thread_panel_from_message(source_message)
        self.input_thread_name(thread_name)
        self.send_starter_message(starter_message)
        self.verify_thread_in_sidebar(thread_name)
        self.verify_source_message_in_thread(source_message)
        self.verify_starter_message_in_thread(starter_message)
        self.verify_thread_created_system_message(thread_name)
        self.close_thread_panel()
        self.verify_thread_in_thread_list(thread_name, starter_message)
        self.dismiss_overlays()
        self.ensure_channel_view()

        return thread_name, starter_message

    # =========================================================================
    # CREATE PUBLIC THREAD FROM THREAD LIST
    # =========================================================================

    def open_thread_list(self):
        self.dismiss_overlays()
        self.ensure_channel_view()
        header = self.wait.until(
            EC.presence_of_element_located(self.THREADS_HEADER_BUTTON)
        )
        button = header.find_element(By.TAG_NAME, "button")

        deadline = time.time() + 30
        while time.time() < deadline:
            self._js_click(button)
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
        self._js_click(create_button)

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
                if item.is_displayed() and self._thread_name_matches(thread_name, item.text):
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

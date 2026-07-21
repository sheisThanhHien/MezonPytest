import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.thread_base_page import ThreadBasePage


class ThreadFromMessagePage(ThreadBasePage):
    CREATE_THREAD_HOVER_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-hover_message_actions-button-base']",
    )

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

    def open_create_thread_panel(self, source_message):
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

    def create_thread(self, source_message, thread_name, starter_message):
        self.validate_thread_name(thread_name)

        if not starter_message.strip():
            raise ValueError("Starter message is required.")

        self.open_create_thread_panel(source_message)
        self.input_thread_name(thread_name)
        self.send_starter_message(starter_message)

        return thread_name, starter_message

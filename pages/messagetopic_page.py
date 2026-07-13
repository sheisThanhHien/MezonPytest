import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.message_page import MessagePage


class MessageTopicPage(MessagePage):
    TOPIC_HEADER = (By.CSS_SELECTOR, "[data-e2e='chat-topic-header']")
    TOPIC_HEADER_CLOSE_BUTTON = (By.CSS_SELECTOR, "[data-e2e='chat-topic-header-button-close']")   
    TOPIC_VIEW_BUTTON = (
        By.CSS_SELECTOR,
        "[data-e2e='chat-topic-button-view_topic']",
    )
    TOPIC_DISCUSSION_BOX = (
        By.CSS_SELECTOR,
        "[data-e2e='discussion-box-topic']",
    )
    TOPIC_MENU_ICON_PATH = "M5.5 12C5.49988"

    def open_topic_discussion(self, message):
        message_item = self._find_message_item_by_text(message)
        self._open_context_menu(message_item)
        self.wait.until(lambda driver: self._get_visible_context_menu() is not None)
        self._click_context_menu_item(self.TOPIC_MENU_ICON_PATH)
        self.wait.until(EC.visibility_of_element_located(self.TOPIC_HEADER))
        self.wait.until(
            EC.visibility_of_element_located(self.TOPIC_DISCUSSION_BOX)
        )
        return message_item

    def send_topic_message(self, topic_message):
        discussion_box = self.wait.until(
            EC.visibility_of_element_located(self.TOPIC_DISCUSSION_BOX)
        )
        chat_input = discussion_box.find_element(*self.CHAT_INPUT)
        chat_input.click()
        chat_input.send_keys(topic_message)
        chat_input.send_keys(Keys.ENTER)

    def verify_view_topic_label(self):
        view_topic = self.wait.until(
            EC.visibility_of_element_located(self.TOPIC_VIEW_BUTTON)
        )
        if not view_topic.is_displayed():
            raise AssertionError("View topic label is not displayed.")
        return view_topic

    def verify_topic_message_sent(self, topic_message):
        deadline = time.time() + 120

        while time.time() < deadline:
            discussion_boxes = [
                box
                for box in self.driver.find_elements(*self.TOPIC_DISCUSSION_BOX)
                if box.is_displayed()
            ]
            if not discussion_boxes:
                time.sleep(1)
                continue

            discussion_box = discussion_boxes[-1]
            if topic_message in discussion_box.text:
                return topic_message

            time.sleep(1)

        raise AssertionError(
            f"Could not find topic message '{topic_message}' in topic chat."
        )

    def create_topic(self, source_message, topic_message):
        self.open_topic_discussion(source_message)
        self.send_topic_message(topic_message)
        self.verify_topic_message_sent(topic_message)
        self.verify_view_topic_label()
        return topic_message

    def close_topic(self):
        self.wait.until(EC.visibility_of_element_located(self.TOPIC_HEADER_CLOSE_BUTTON))
        self.driver.find_element(*self.TOPIC_HEADER_CLOSE_BUTTON).click()

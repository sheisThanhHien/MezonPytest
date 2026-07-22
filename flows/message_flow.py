import time

from pages.channel_page import ChannelPage
from pages.message_page import MessagePage
from pages.messageedit_page import MessageEditPage
from pages.messagepin_page import MessagePinPage
from pages.messagetopic_page import MessageTopicPage
from utils.helpers import get_current_time


def send_text_message(driver, wait, channel_name=None):
    if channel_name:
        ChannelPage(driver, wait).open_channel(channel_name)

    message = "Pytest " + get_current_time()

    message_page = MessagePage(driver, wait)
    message_page.send_message(message)
    message_page.verify_message_sent(message)

    return message

def send_multiline_message(driver, wait, channel_name=None):
    if channel_name:
        ChannelPage(driver, wait).open_channel(channel_name)

    timestamp = get_current_time()
    message = f"Pytest line 1 {timestamp}\nPytest line 2 {timestamp}"

    message_page = MessagePage(driver, wait)
    message_page.send_multiline_message(message)
    message_page.verify_message_sent(message)

    return message

def edit_text_message(driver, wait, original_message, new_message=None):
    if new_message is None:
        new_message = "Edited " + get_current_time()

    message_edit_page = MessageEditPage(driver, wait)
    message_edit_page.edit_message(original_message, new_message)
    message_edit_page.verify_message_text(new_message)

    return new_message

def pin_message(driver, wait, message):
    message_pin_page = MessagePinPage(driver, wait)
    message_pin_page.pin_message(message)
    message_pin_page.verify_message_pinned(message)

    return message


def create_topic_from_message(driver, wait, source_message, topic_message=None):
    if topic_message is None:
        topic_message = "Topic " + get_current_time()

    message_topic_page = MessageTopicPage(driver, wait)
    message_topic_page.create_topic(source_message, topic_message)
    message_topic_page.close_topic()

    return topic_message


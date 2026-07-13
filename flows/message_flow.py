import time

from pages.channel_page import ChannelPage
from pages.message_page import MessagePage
from pages.messageedit_page import MessageEditPage
from pages.messagepin_page import MessagePinPage
from utils.helpers import get_current_time


def send_text_message(driver, wait, channel_name=None):
    if channel_name:
        ChannelPage(driver, wait).open_channel(channel_name)

    message = "Pytest " + get_current_time()

    message_page = MessagePage(driver, wait)
    message_page.send_message(message)
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
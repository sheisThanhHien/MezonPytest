import time

from pages.channel_page import ChannelPage
from utils.helpers import get_current_time


def create_text_channel(driver, wait, category_name=None):
    channel_page = ChannelPage(driver, wait)
    channel_page.click_create_channel_button(category_name)
    channel_page.click_text_channel_type()
    channel_name = "Text Channel " + get_current_time()
    channel_page.input_channel_name(channel_name)
    channel_page.click_confirm_create_channel()
    time.sleep(1)
    channel_page.verify_channel_created(channel_name, category_name)

    return channel_name
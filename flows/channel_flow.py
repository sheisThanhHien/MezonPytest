import time

from pages.channel_page import ChannelPage
from pages.channeledition_page import ChannelEditionPage
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


def edit_text_channel_name(driver, wait, channel_name, new_channel_name):
    channeledition_page = ChannelEditionPage(driver, wait)
    channeledition_page.open_channel_context_menu(channel_name)
    channeledition_page.click_edit_channel_option()
    channeledition_page.input_channel_name(new_channel_name)
    channeledition_page.click_save_changes_button()
    channeledition_page.verify_sidebar_new_channel_name(new_channel_name)

    return new_channel_name
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages import clancreation_page
from pages.channel_page import ChannelPage


from utils.helpers import get_current_time


def create_text_channel(driver, wait):
    channel_page = ChannelPage(driver, wait)
    channel_page.click_create_channel_button()
    channel_page.click_text_channel_type()
    channel_name = "Text Channel " + get_current_time()
    channel_page.input_channel_name(channel_name)
    channel_page.click_confirm_create_channel()

    channel_page.verify_channel_created(channel_name)

    return channel_name

# def delete_channel(driver, wait, channel_name):
#     channel_page = ChannelPage(driver, wait)
#     channel_page.click_delete_channel_button()
#     channel_page.click_confirm_delete_channel()
#     return channel_name
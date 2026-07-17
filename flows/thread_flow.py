from pages.thread_page import ThreadPage
from utils.helpers import get_current_time


def create_public_thread_from_thread_list(driver, wait, thread_name=None, starter_message=None):
    if thread_name is None:
        thread_name = "Thread " + get_current_time()

    if starter_message is None:
        starter_message = "Starter " + get_current_time()

    thread_page = ThreadPage(driver, wait)
    thread_page.create_public_thread(thread_name, starter_message)
    thread_page.verify_thread_in_sidebar(thread_name)
    thread_page.verify_thread_created_system_message(thread_name)
    thread_page.verify_starter_message_in_thread(starter_message)

    thread_page.close_thread_panel()
    thread_page.verify_thread_in_thread_list(thread_name, starter_message)
    thread_page.jump_to_thread_from_system_message(thread_name)
    thread_page.verify_jump_to_thread(thread_name, starter_message)

    return thread_name, starter_message

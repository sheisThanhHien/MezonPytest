from pages.thread_from_message_page import ThreadFromMessagePage
from pages.thread_list_page import ThreadListPage
from utils.helpers import get_current_time


def _build_thread_data(thread_name, starter_message):
    if thread_name is None:
        thread_name = "Thread " + get_current_time()

    if starter_message is None:
        starter_message = "Starter " + get_current_time()

    return thread_name, starter_message


def _verify_thread_created(driver, wait, page, thread_name, starter_message, source_message=None):
    page.verify_thread_in_sidebar(thread_name)

    if source_message:
        page.verify_source_message_in_thread(source_message)

    page.verify_starter_message_in_thread(starter_message)
    page.verify_thread_created_system_message(thread_name)
    page.close_thread_panel()

    list_page = ThreadListPage(driver, wait)
    list_page.verify_thread_in_thread_list(thread_name, starter_message)


def create_public_thread_from_thread_list(
    driver,
    wait,
    thread_name=None,
    starter_message=None,
):
    thread_name, starter_message = _build_thread_data(thread_name, starter_message)

    thread_page = ThreadListPage(driver, wait)
    thread_page.dismiss_overlays()
    thread_page.create_public_thread(thread_name, starter_message)
    _verify_thread_created(driver, wait, thread_page, thread_name, starter_message)
    thread_page.jump_to_thread_from_system_message(thread_name)
    thread_page.verify_jump_to_thread(thread_name, starter_message)
    thread_page.close_thread()

    return thread_name, starter_message


def create_thread_from_message(
    driver,
    wait,
    source_message,
    thread_name=None,
    starter_message=None,
):
    thread_name, starter_message = _build_thread_data(thread_name, starter_message)

    thread_page = ThreadFromMessagePage(driver, wait)
    thread_page.dismiss_overlays()
    thread_page.create_thread(source_message, thread_name, starter_message)
    _verify_thread_created(
        driver,
        wait,
        thread_page,
        thread_name,
        starter_message,
        source_message=source_message,
    )
    thread_page.dismiss_overlays()
    thread_page.ensure_channel_view()

    return thread_name, starter_message

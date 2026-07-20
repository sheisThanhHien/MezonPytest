import pytest

from utils.helpers import get_current_time
from utils.e2e_report import e2e_section
from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.category_flow import create_category, edit_category
from flows.channel_flow import create_text_channel
from flows.message_flow import (
    send_text_message,
    edit_text_message,
    pin_message,
    create_topic_from_message,
)
from flows.thread_flow import (
    create_public_thread_from_thread_list,
    create_thread_from_message,
)


@pytest.mark.e2e
@pytest.mark.regression
def test_mezon_full_flow(driver, wait):
    with e2e_section("LOGIN") as section:
        login_email_password(driver, wait)
        section.add("Login successfully!")

    with e2e_section("CREATE CLAN") as section:
        clan_name = create_clan(driver, wait)
        section.add(f"Created clan: {clan_name}")
        section.add("Clan verified")

    with e2e_section("CREATE CATEGORY") as section:
        category_name = create_category(driver, wait)
        section.add(f"Created category: {category_name}")
        section.add("Category verified")

    with e2e_section("EDIT CATEGORY") as section:
        edited_category_name = "Category Edited " + get_current_time()
        edit_category(driver, wait, category_name, edited_category_name)
        section.add(f"Edited: {category_name} -> {edited_category_name}")
        section.add("Category edit verified")

    with e2e_section("CREATE TEXT CHANNEL") as section:
        channel_name = create_text_channel(driver, wait, edited_category_name)
        section.add(
            f"Created channel: {channel_name} in category: {edited_category_name}"
        )
        section.add("Text channel verified")

    with e2e_section("SEND TEXT MESSAGE") as section:
        message = send_text_message(driver, wait, channel_name)
        section.add(f"Sent message: {message}")
        section.add("Message verified")

    with e2e_section("EDIT MESSAGE") as section:
        edited_message = edit_text_message(driver, wait, message)
        section.add(f"Edited message: {message} -> {edited_message}")
        section.add("Edited message verified")

    with e2e_section("PIN MESSAGE") as section:
        pinned_message = pin_message(driver, wait, edited_message)
        section.add(f"Pinned message: {edited_message} -> {pinned_message}")
        section.add("Pinned message verified")

    with e2e_section("CREATE TOPIC") as section:
        topic_message = create_topic_from_message(driver, wait, edited_message)
        section.add(f"Created topic: {edited_message} -> {topic_message}")
        section.add("Topic message verified")

    with e2e_section("CREATE THREAD FROM MESSAGE") as section:
        thread_name, starter_message = create_thread_from_message(
            driver,
            wait,
            edited_message,
        )
        section.add(f"Created thread: {thread_name}")
        section.add(f"Starter message: {starter_message}")
        section.add("Thread verified in sidebar and thread list")
        section.add("System message verified")
        section.add("Source message and starter message verified")

    with e2e_section("CREATE PUBLIC THREAD FROM THREAD LIST") as section:
        thread_name, starter_message = create_public_thread_from_thread_list(
            driver, wait
        )
        section.add(f"Created thread: {thread_name}")
        section.add(f"Starter message: {starter_message}")
        section.add("Thread verified in sidebar and thread list")
        section.add("System message and jump to thread verified")


    with e2e_section("DELETE CLAN") as section:
        delete_clan(driver, wait, clan_name)
        section.add(f"Deleted clan: {clan_name}")

import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.message_flow import send_text_message
from flows.thread_flow import create_thread_from_message


@pytest.mark.messages
@pytest.mark.regression

def test_create_thread_from_message(driver, wait):
    login_email_password(driver, wait)
    print("Login successfully!")

    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")

    source_message = send_text_message(driver, wait)
    print(f"Sent message: {source_message}")

    thread_name, starter_message = create_thread_from_message(
        driver,
        wait,
        source_message,
    )
    print(f"Created thread: {thread_name}")
    print(f"Starter message: {starter_message}")
    print("Thread verified in sidebar and thread list")
    print("System message verified")
    print("Source message and starter message verified")

    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

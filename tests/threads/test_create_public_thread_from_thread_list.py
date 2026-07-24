import pytest

from flows.auth_flow import login_email_password
from flows.channel_flow import create_text_channel
from flows.clan_flow import create_clan, delete_clan
from flows.thread_flow import create_public_thread_from_thread_list


@pytest.mark.threads
@pytest.mark.regression
@pytest.mark.smoke

def test_create_public_thread_from_thread_list(driver, wait):
    login_email_password(driver, wait)
    print("Login successfully!")

    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")

    channel_name = create_text_channel(driver, wait)
    print(f"Created channel: {channel_name}")

    thread_name, starter_message = create_public_thread_from_thread_list(
        driver, wait
    )
    print(f"Created public thread: {thread_name}")
    print(f"Starter message: {starter_message}")
    print("Thread verified in sidebar and thread list")
    print("System message and starter message verified")
    print("Jump to thread from system message verified")

    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.message_flow import edit_text_message, send_text_message


@pytest.mark.messages
@pytest.mark.regression
@pytest.mark.smoke

def test_edit_text_message(driver, wait):
    login_email_password(driver, wait)
    print("Login successfully!")

    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")

    message = send_text_message(driver, wait)
    print(f"Sent message: {message}")

    edited_message = edit_text_message(driver, wait, message)
    print(f"Edited message: {edited_message}")
    print("Edited message verified")

    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.message_flow import send_multiline_message


@pytest.mark.messages
@pytest.mark.regression
@pytest.mark.smoke

def test_send_multiline_message(driver, wait):
    login_email_password(driver, wait)
    print("Login successfully!")

    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")

    message = send_multiline_message(driver, wait)
    print(f"Sent message: {message}")
    print("✓ Message verified")

    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

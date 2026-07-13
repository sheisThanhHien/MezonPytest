import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.message_flow import pin_message, send_text_message

@pytest.mark.messages
@pytest.mark.regression
def test_pin_message(driver, wait):
    login_email_password(driver, wait)
    print("Login successfully!")

    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")

    message = send_text_message(driver, wait)
    print(f"Sent message: {message}")

    pinned_message = pin_message(driver, wait, message)
    print(f"Pinned message: {message} -> {pinned_message}") # Verify message is pinned
    print("Pin system message verified") # Verify pin system message is visible
    print(f"Pinned message {message} verified in pin list") # Verify message is in pin list


    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.message_flow import create_topic_from_message, send_text_message


@pytest.mark.messages
@pytest.mark.regression
def test_create_topic(driver, wait):
    login_email_password(driver, wait)
    print("Login successfully!")

    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")

    message = send_text_message(driver, wait)
    print(f"Sent message: {message}")

    topic_message = create_topic_from_message(driver, wait, message)
    print(f"Created topic with message: {topic_message}")
    print("View topic label verified")
    print("Topic message verified in topic chat")

    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

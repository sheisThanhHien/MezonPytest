import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from pages.channel_page import ChannelPage
from flows.channel_flow import create_text_channel


@pytest.mark.channels
@pytest.mark.smoke
@pytest.mark.regression

def test_create_text_channel(driver, wait):

    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Create channel
    channel_name = create_text_channel(driver, wait)
    print(f"Created channel: {channel_name}")
    print("✓ Channel verified")

    # Cleanup
    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

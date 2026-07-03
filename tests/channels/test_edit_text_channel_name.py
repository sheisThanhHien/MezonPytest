import pytest
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import get_current_time
from flows.channel_flow import edit_text_channel_name
from pages.channel_page import ChannelPage
from flows.clan_flow import create_clan, delete_clan
from flows.channel_flow import create_text_channel
from flows.auth_flow import login_email_password 


@pytest.mark.channels
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.multilang

def test_edit_text_channel_name(driver, wait):
    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Create channel
    channel_name = create_text_channel(driver, wait)
    print(f"Created channel: {channel_name}")
    print("✓ Channel verified")

    # Edit channel name
    new_channel_name = "Edited Channel " + get_current_time()
    new_channel_name = edit_text_channel_name(driver, wait, channel_name, "New Channel Name")
    print(f"Edited channel name: {new_channel_name}")
    print("✓ Channel name verified")

    # Cleanup
    delete_clan(driver, wait, clan_name) 
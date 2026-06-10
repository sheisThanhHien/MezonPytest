import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from flows.auth_flow import login_email_password
from flows.channel_flow import create_text_channel
from flows.clan_flow import create_clan, delete_clan


@pytest.mark.channels
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.multilang
def test_create_text_channel(driver, wait):

    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Create channel
    channel_name = create_text_channel(driver, wait)

    # Verify channel created
    # channel_items = wait.until(
    #     EC.presence_of_all_elements_located(
    #         (By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-item']")
    #     )
    # )
    # is_found = False
    # target_name = channel_name.upper()

    # for item in channel_items:
    #     actual_channel = item.text.strip().upper()
    #     print(f"Checking Channel: '{actual_channel}'")

    #     if target_name in actual_channel:
    #         is_found = True
    #         break

    # assert is_found, f"Channel '{target_name}' not found"
    # print(f"Channel '{target_name}' found")

    # Delete clan
    delete_clan(driver, wait, clan_name)
    print(f"Clan '{clan_name}' deleted")
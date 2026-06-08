from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan


def test_create_clan(driver, wait):

    # Login
    login_email_password(driver, wait)

    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='button-base']")
        )
    )

    # Create clan
    clan_name = create_clan(driver, wait)

    # Verify clan created
    header_clan_name = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']")
        )
    ).text.strip() 

    assert header_clan_name == clan_name.upper(), f"Clan name mismatch. Expected '{clan_name.upper()}', got '{header_clan_name}'." 

    # Cleanup
    delete_clan(driver, wait, clan_name)
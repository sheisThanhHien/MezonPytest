import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan


@pytest.mark.clans
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.multilang
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
    print(f"Created clan: {clan_name}")
    print("✓ Clan verified")

    # Cleanup
    delete_clan(driver, wait, clan_name)
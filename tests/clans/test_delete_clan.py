import pytest
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan


@pytest.mark.clans
@pytest.mark.regression
@pytest.mark.multilang
def test_delete_clan(driver, wait):
    login_email_password(driver, wait)

    clan_name = create_clan(driver, wait)

    delete_clan(driver, wait, clan_name)

    clan_containers = driver.find_elements(
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-side_bar-clan_item']",
    )
    target_name = clan_name.upper()
    is_found = False
    for container in clan_containers:
        try:
            if target_name in container.text.strip().upper():
                is_found = True
                break
        except StaleElementReferenceException:
            continue

    assert not is_found, f"Clan '{target_name}' still exists after deletion"

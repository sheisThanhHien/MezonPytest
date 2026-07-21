import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan


@pytest.mark.clans
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.multilang
def test_create_clan(driver, wait):
    login_email_password(driver, wait)
    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")
    print("Clan verified")
    delete_clan(driver, wait, clan_name)

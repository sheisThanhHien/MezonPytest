import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan


@pytest.mark.clans
@pytest.mark.regression
@pytest.mark.multilang
def test_delete_clan(driver, wait):
    login_email_password(driver, wait)
    clan_name = create_clan(driver, wait)
    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")
    print("Clan removed from sidebar verified")

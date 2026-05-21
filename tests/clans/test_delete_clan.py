from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan


def test_delete_clan(driver, wait):

    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Delete clan
    delete_clan(driver, wait, clan_name)

    # TODO:
    # verify clan deleted
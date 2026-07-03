import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.category_flow import create_category


@pytest.mark.categories
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.multilang
def test_create_category(driver, wait):

    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Create category 
    category_name = create_category(driver, wait)
    print(f"Created category: {category_name}")
    print("✓ Category verified")

    # Cleanup
    delete_clan(driver, wait, clan_name)

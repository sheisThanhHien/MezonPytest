import pytest

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.category_flow import create_category, edit_category
from utils.helpers import get_current_time

@pytest.mark.categories
@pytest.mark.regression

def test_edit_category(driver, wait):

    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Create category
    category_name = create_category(driver, wait)

    # Edit category
    new_category_name = "Edited Category " + get_current_time()
    
    edit_category(driver, wait, category_name, new_category_name)
    print(f"Old category: {category_name}")
    print(f"New category: {new_category_name}")
    
    # Cleanup
    delete_clan(driver, wait, clan_name)

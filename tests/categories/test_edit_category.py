import pytest
from selenium.webdriver.common.by import By

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.category_flow import create_category, edit_category
from utils.helpers import get_current_time


@pytest.mark.categories
@pytest.mark.regression
@pytest.mark.multilang
def test_edit_category(driver, wait):

    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Create category
    category_name = create_category(driver, wait)

    # Edit category
    new_category_name = "Edited Category " + get_current_time()
    
    edit_category(
        driver,
        wait,
        category_name,
        new_category_name
    )
    print(f"Old category: {category_name}")
    print(f"New category: {new_category_name}")

    # # Verify edited category
    # category_containers = driver.find_elements(
    #     By.CSS_SELECTOR,
    #     "[data-e2e='clan_page-side_bar-channel_list-category']"
    # )

    # is_found = False

    # target_edited_name = new_category_name.upper()

    # for container in category_containers:

    #     try:

    #         name_element = container.find_element(
    #             By.CSS_SELECTOR,
    #             "[data-e2e='clan_page-side_bar-channel_list-category-name']"
    #         )

    #         actual_category = name_element.text.strip().upper()

    #         if target_edited_name in actual_category:

    #             is_found = True

    #             break

    #     except:
    #         continue

    # assert is_found
    
    # Cleanup
    delete_clan(driver, wait, clan_name)

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.category_flow import create_category, edit_category
from utils.helpers import get_current_time


def _category_exists(driver, wait, category_name):
    category_containers = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']")
        )
    )
    target_name = category_name.upper()
    for container in category_containers:
        try:
            name_element = container.find_element(
                By.CSS_SELECTOR,
                "[data-e2e='clan_page-side_bar-channel_list-category-name']",
            )
            if target_name in name_element.text.strip().upper():
                return True
        except StaleElementReferenceException:
            continue
    return False


def test_mezon_full_flow(driver, wait):
    
    # LOGIN
    print("\n========== LOGIN ==========")
    login_email_password(driver, wait)
    print("Login successfully!")

    # CREATE CLAN
    print("\n========== CREATE CLAN ==========")
    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")

    # VERIFY CLAN CREATED
    header_clan_name = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']")
        )
    ).text.strip()
    print(f"Actual clan header: {header_clan_name}")
    assert header_clan_name == clan_name.upper(), (
        f"Clan name mismatch. Expected '{clan_name.upper()}', got '{header_clan_name}'."
    )
    print("✓ Clan verified")
    
    # CREATE CATEGORY
    print("\n========== CREATE CATEGORY ==========")
    category_name = create_category(driver, wait)
    print(f"Created category: {category_name}")

    # VERIFY CATEGORY CREATED
    assert _category_exists(driver, wait, category_name), (
        f"Cannot find category '{category_name.upper()}'"
    )
    print("✓ Category verified")

    # EDIT CATEGORY
    print("\n========== EDIT CATEGORY ==========")
    edited_category_name = "Category Edited " + get_current_time()
    print(f"New category name: {edited_category_name}")

    edit_category(
        driver, 
        wait, 
        category_name, 
        edited_category_name)

    # VERIFY CATEGORY EDITED
    assert _category_exists(
        driver, 
        wait, 
        edited_category_name), (
        f"Cannot find edited category '{edited_category_name.upper()}'"
    )
    print("✓ Category edit verified")


    # Delete clan
    print("\n========== DELETE CLAN ==========")

    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")

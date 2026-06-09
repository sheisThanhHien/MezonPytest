from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.category_flow import create_category


def test_create_category(driver, wait):

    # Login
    login_email_password(driver, wait)

    # Create clan
    clan_name = create_clan(driver, wait)

    # Create category
    category_name = create_category(driver, wait)

    # Verify category created
    category_containers = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']")
        )
    )    
    is_found = False

    target_name = category_name.upper()

    for container in category_containers:

        try:

            name_element = container.find_element(
                By.CSS_SELECTOR,
                "[data-e2e='clan_page-side_bar-channel_list-category-name']"
            )

            actual_category = name_element.text.strip().upper()

            print(f"Checking Category: '{actual_category}'")

            if target_name == actual_category:

                is_found = True
                
                print(f"✅ Found Category: {name_element.text}")

                break

        except Exception as e:
            print(f"Error checking category: {e}")
            continue

    assert is_found, f"Cannot find category '{target_name}'"
    print(f"Category '{target_name}' found")

    # Cleanup
    delete_clan(driver, wait, clan_name)
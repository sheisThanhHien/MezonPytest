import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from utils.helpers import get_current_time


def create_category(driver, wait):

    # Open clan menu
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))).click()

    # Open menu items
    clan_settings_menu = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']")
        )
    )

    # Show empty categories
    clan_settings_menu[5].click()

    time.sleep(0.5)

    # Create category
    clan_settings_menu[0].click()

    create_category_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-input-category_name']")
        )
    )

    category_name = "Category " + get_current_time()

    create_category_input.send_keys(category_name)

    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-button-confirm']")
        )
    ).click()

    return category_name

def edit_category(driver, wait, old_category_name, new_category_name):

    category_containers = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']")
        )
    )

    target_container = None

    old_name_upper = old_category_name.upper()

    for container in category_containers:

        try:
            name_element = container.find_element(
                By.CSS_SELECTOR,
                "[data-e2e='clan_page-side_bar-channel_list-category-name']"
            )

            if old_name_upper in name_element.text.strip().upper():

                target_container = container

                break

        except:
            continue

    assert target_container is not None

    actions = ActionChains(driver)

    actions.context_click(target_container).perform()

    time.sleep(0.5)

    edit_option = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-panel-item']")
        )
    )

    edit_option.click()

    edit_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-modal-edit_category-input-name']")
        )
    )

    edit_input.clear()

    edit_input.send_keys(new_category_name)

    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='clan_page-modal-edit_category-button-confirm']")
        )
    ).click()
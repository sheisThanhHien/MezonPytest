import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from flows.auth_flow import login_email_password


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.regression
def test_mezon_login_success(driver, wait):
    # Login
    login_email_password(driver, wait)
    # Verify login success
    login_success_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-e2e='button-base']")
        )
    )

    assert login_success_button is not None
import pytest

from flows.auth_flow import login_email_password


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.regression
def test_mezon_login_success(driver, wait):
    login_email_password(driver, wait)
    print("Login successfully verified")

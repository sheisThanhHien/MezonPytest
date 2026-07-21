from constants import EMAIL, PASSWORD
from pages.auth_page import AuthPage


def login_email_password(driver, wait):
    auth_page = AuthPage(driver, wait)
    auth_page.login_with_email_password(EMAIL, PASSWORD)
    auth_page.verify_logged_in()

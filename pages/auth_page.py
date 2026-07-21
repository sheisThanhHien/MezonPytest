from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from constants import BASE_URL
from pages.base_page import BasePage


class AuthPage(BasePage):
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    EMAIL_PASSWORD_OPTION = (By.LINK_TEXT, "Login with Email and Password")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "login_password")
    SUBMIT_BUTTON = (By.ID, "sendOtpBtn")
    LOGGED_IN_INDICATOR = (
        By.CSS_SELECTOR,
        "[data-e2e='clan_page-side_bar-button-add_clan']",
    )
    SPLASH_SCREEN = (By.CSS_SELECTOR, ".splash-screen")

    def open_app(self):
        self.driver.get(BASE_URL)

    def login_with_email_password(self, email, password):
        self.open_app()
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK)).click()
        self.wait.until(
            EC.element_to_be_clickable(self.EMAIL_PASSWORD_OPTION)
        ).click()
        email_field = self.wait.until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_field.send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()

    def verify_logged_in(self):
        self.wait.until(EC.invisibility_of_element_located(self.SPLASH_SCREEN))
        self.wait.until(
            EC.presence_of_element_located(self.LOGGED_IN_INDICATOR)
        )

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



class CreateClanModal:
    # Locators

    CREATE_CLAN_BUTTON = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-button-add_clan']"
    )

    CREATE_CLAN_MODAL = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan']"
    )

    OPTION_CREATE_MY_OWN = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-template-item-create_my_own']"
    )

    MODAL_CLAN_NAME_INPUT = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_clan-input-clan_name']"
    )

    CREATE_CLAN_BUTTON_BASE = (
        By.CSS_SELECTOR,"button[data-e2e='button-base']"
    )

    CLAN_HEADER = (
        By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"
    )

    # CONSTRUCTORS
    def __init__ (self, driver, wait):
            self.driver = driver
            self.wait = wait

    # ACTIONS
    def click_create_clan_button(self):
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".splash-screen"))
        )
        button = self.wait.until(
            EC.presence_of_element_located(self.CREATE_CLAN_BUTTON)
        )
        try:
            self.wait.until(
                EC.element_to_be_clickable(self.CREATE_CLAN_BUTTON)
            ).click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", button)

    def wait_create_clan_modal_visible(self):
        return self.wait.until(
            EC.presence_of_element_located(
                self.CREATE_CLAN_MODAL
            )
        )

    def click_create_my_own_option(self):

        self.wait.until(
            EC.element_to_be_clickable(
                self.OPTION_CREATE_MY_OWN
            )
        ).click()

    def input_clan_name(self, clan_name):

        self.wait.until(
            EC.presence_of_element_located(
                self.MODAL_CLAN_NAME_INPUT
            )
        ).send_keys(clan_name)

    def click_confirm_create_clan(self):
        modal = self.wait_create_clan_modal_visible()
        buttons = modal.find_elements(
            *self.CREATE_CLAN_BUTTON_BASE
        )
        create_button = buttons[-1]
        self.wait.until(
            lambda d: create_button.is_enabled()
        )
        create_button.click()

    def verify_clan_created(self, clan_name):
        target = clan_name.upper()
        return self.wait.until(
            lambda d: d.find_element(*self.CLAN_HEADER).text.strip().upper() == target
        )

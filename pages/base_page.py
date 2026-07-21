import time

from selenium.common.exceptions import StaleElementReferenceException


class BasePage:
    POLL_TIMEOUT = 120
    POLL_INTERVAL = 1

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def js_click(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)

    def poll_until(self, condition, error_message, timeout=POLL_TIMEOUT):
        deadline = time.time() + timeout

        while time.time() < deadline:
            try:
                result = condition()
                if result:
                    return result
            except StaleElementReferenceException:
                pass

            time.sleep(self.POLL_INTERVAL)

        raise AssertionError(error_message)

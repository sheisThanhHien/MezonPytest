import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



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



    # ================================================
    # Mouse Actions
    # ================================================
    def hover(self, element):
        """Hover chuột vào element"""
        ActionChains(self.driver).move_to_element(element).perform()

    def click_element(self, element):
        """Click trực tiếp vào WebElement"""
        element.click()

    def double_click(self, element):
        """Double click"""
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, element):
        """Right click"""
        ActionChains(self.driver).context_click(element).perform()

    def drag_and_drop(self, source, target):
        """Kéo thả"""
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    # ========================
    # Keyboard Actions
    # ========================

    def press_enter(self, element):
        element.send_keys(Keys.ENTER)

    def press_shift_enter(self, element):
        element.send_keys(Keys.SHIFT, Keys.ENTER)

    def press_escape(self, element):
        element.send_keys(Keys.ESCAPE)

    def press_tab(self, element):
        element.send_keys(Keys.TAB)

    # ========================
    # Scroll
    # ========================

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_middle(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

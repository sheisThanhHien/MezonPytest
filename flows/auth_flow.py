from constants import BASE_URL, EMAIL, PASSWORD
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def login_email_password(driver, wait):
    driver.get(BASE_URL)
    login_homepage_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
    login_homepage_btn.click()

    # driver.refresh()
    
    email_password_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login with Email and Password")))
    email_password_option.click()
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys(EMAIL)
    password_field = driver.find_element(By.NAME, "login_password")
    password_field.send_keys(PASSWORD)
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "sendOtpBtn")))
    login_btn.click()
    

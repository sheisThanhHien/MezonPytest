import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from helpers import get_current_time, login_email_password, create_clan, delete_clan

def create_category(driver, wait):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))).click()    
    clan_settings_menu = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']")))

    show_empty_categories_option = clan_settings_menu[5].click() 
    create_category_option = clan_settings_menu[0].click()    
    create_category_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-input-category_name']")))
    category_name = "Category " + get_current_time()
    create_category_input.send_keys(category_name)    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-button-confirm']"))).click()

    return category_name


def test_create_category():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait[WebDriverWait](driver, 15)

    try:
        # Login
        login_email_password(driver, wait)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))
        print("Login Successfully!")

        # Create Clan
        # create_clan(driver, wait)
        clan_name = create_clan(driver, wait)

        # Create Category
        category_name = create_category(driver, wait)
        
        print(f"Created Category Name: {category_name}")

        expected_category_name = category_name.upper()
        category_xpath = f"//*[@data-e2e='clan_page-side_bar-channel_list-category-name' and text()='{expected_category_name}']" 
        exact_category_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, category_xpath))
        )

        assert exact_category_element.is_displayed(), f"Thất bại: Không tìm thấy Category '{expected_category_name}' trên giao diện!"
        
        print(f"Verify thành công: Đã tìm thấy đúng Category mới tạo: {exact_category_element.text}")

        # category_name_channel_list = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category-name']"))).text
        # assert category_name_channel_list == category_name.upper(), (
        #     f"Category name mismatch. Expected '{category_name.upper()}', got '{category_name_channel_list}'.")

        
        # print("Category created successfully.")

        time.sleep(3)
        
        
        # Delete Clan
        delete_clan(driver, wait, clan_name)


    except Exception as e:
        print(f"RESULT: Failed due to - {repr(e)}")
        driver.save_screenshot("evidence/test_create_category.png")
        raise        

    finally:
        time.sleep(7)
        driver.quit()    

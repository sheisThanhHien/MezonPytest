import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from helpers import get_current_time, login_email_password, create_clan, delete_clan

def create_category(driver, wait):
    # Open Clan Menu 
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-header-title-clan_name']"))).click()    
    
    # select Show Empty 
    clan_settings_menu = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-header-modal_panel-item']")))
    show_empty_categories_option = clan_settings_menu[5].click() 

    time.sleep(0.5)

    # Select Create Category 
    create_category_option = clan_settings_menu[0].click()    
    create_category_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-input-category_name']")))
    category_name = "Category " + get_current_time()
    create_category_input.send_keys(category_name)    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-create_category-button-confirm']"))).click()

    return category_name



def test_create_category():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

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

        
        time.sleep(2)

        # Div ngoai 
        category_containers = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']")
        
        is_found = False          # Tạo một biến "đánh dấu" để biết đã tìm thấy hay chưa
        target_name = category_name.upper()

        for container in category_containers:
            try: 
                name_element = container.find_element(By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category-name']")
                
                actual_category = name_element.text.strip().upper()
                
                print(f"Checking category: '{actual_category}'")

                if target_name in actual_category:
                    is_found = True
                    print(f"✅ Category founded: {name_element.text}")
                    break
            except:
                continue                            # Nếu một cụm div nào đó không có thẻ name bên trong thì bỏ qua

        # 4. Chốt kết quả
        assert is_found, f"❌ FAILED: Cannot find '{target_name}' !"

        time.sleep(2)
        
        
        # Delete Clan
        # delete_clan(driver, wait, clan_name)


    except Exception as e:
        print(f"RESULT: Failed due to - {repr(e)}")
        driver.save_screenshot("evidence/test_create_category.png")
        raise        

    finally:
        time.sleep(7)
        driver.quit()    

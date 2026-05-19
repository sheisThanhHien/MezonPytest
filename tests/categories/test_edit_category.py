import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains   # action right-click


from helpers import get_current_time, login_email_password, create_clan, delete_clan
from tests.categories.test_create_category import create_category

def edit_category(driver, wait, old_category_name, new_category_name):
    """
    Hàm thực hiện luồng CHUỘT PHẢI vào Category cũ và đổi tên trên Mezon
    """
    # 1. Tìm danh sách các khối Category đang hiển thị ở Sidebar
    category_containers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']")))
    
    target_container = None
    old_name_upper = old_category_name.upper() 
    
    for container in category_containers:
        try:
            name_element = container.find_element(By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category-name']")
            if old_name_upper in name_element.text.strip().upper():
                target_container = container
                break
        except:
            continue
            
    assert target_container is not None, f"Không tìm thấy Category cũ có tên '{old_category_name}' để sửa!"

    # 2. THỰC HIỆN CLICK CHUỘT PHẢI (Context Click) VÀO KHỐI CATEGORY
    actions = ActionChains(driver)
    actions.context_click(target_container).perform()
    time.sleep(0.5) # Đợi Context Menu xổ ra ổn định

    # 3. Chọn nút "Edit Category" trong Context Menu vừa hiện ra
    # Bạn hãy check lại data-e2e của nút Edit nằm trong menu chuột phải nhé. 
    # Nếu nút đó dùng chung data-e2e hoặc chỉ có chữ, ta có thể dùng XPath text như sau:

    edit_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-channel_list-panel-item']")))
    
    edit_option.click()

    # 4. Đợi Modal nhập tên hiển thị và điền tên mới
    # (Giả định ô nhập tên mới có data-e2e là: [data-e2e='clan_page-modal-edit_category-input-name'])
    edit_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-edit_category-input-name']")))
    
    edit_input.clear()
    edit_input.send_keys(new_category_name)

    # 5. Click nút Lưu/Xác nhận (Confirm/Save)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='clan_page-modal-edit_category-button-confirm']"))).click()
    time.sleep(1) # Chờ UI cập nhật lại


def test_edit_category():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    clan_name = None

    try:
        # ---- BƯỚC 1: ĐĂNG NHẬP ----
        login_email_password(driver, wait)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-e2e='button-base']")))
        print("1. Login Successfully!")

        # ---- BƯỚC 2: TẠO CLAN ----
        clan_name = create_clan(driver, wait)
        print(f"2. Created Clan Name: {clan_name}")

        # ---- BƯỚC 3: TẠO CATEGORY ----
        category_name = create_category(driver, wait)
        print(f"3. Created Base Category Name: {category_name}")
        time.sleep(2)

        # ---- BƯỚC 4: CHUỘT PHẢI & SỬA TÊN CATEGORY ----
        new_category_name = "Category Edited " + get_current_time()
        edit_category(driver, wait, category_name, new_category_name)
        print(f"4. Requested edit to new name: {new_category_name}")
        time.sleep(2)

        # ---- BƯỚC 5: VERIFY (KIỂM TRA KẾT QUẢ TRÊN UI) ----
        category_containers = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category']")
        is_found = False
        target_edited_name = new_category_name.upper()
        
        for container in category_containers:
            try: 
                name_element = container.find_element(By.CSS_SELECTOR, "[data-e2e='clan_page-side_bar-channel_list-category-name']")
                actual_category = name_element.text.strip().upper()
                if target_edited_name in actual_category:
                    is_found = True
                    print(f"   ➔ Tìm thấy đúng tên Category sau khi sửa trên UI: {name_element.text}")
                    break
            except:
                continue

        assert is_found, f"❌ FAILED: Không tìm thấy Category mang tên mới '{target_edited_name}' sau khi sửa!"
        print("✅ VERIFY THÀNH CÔNG: Tính năng sửa tên Category bằng Chuột phải hoạt động chính xác!")

    except Exception as e:
        print(f"RESULT: Failed due to - {repr(e)}")
        driver.save_screenshot(f"evidence/error_edit_category_{get_current_time().replace(' ', '_')}.png")
        raise        

    finally:
        # ---- BƯỚC 6: TEARDOWN (TỰ ĐỘNG XÓA CLAN ĐỂ DỌN DATA RÁC) ----
        if clan_name:
            print(f"Cleaning up: Deleting clan '{clan_name}'...")
            try:
                delete_clan(driver, wait, clan_name)
            except Exception as delete_error:
                print(f"Không thể dọn dẹp Clan rác do lỗi giao diện: {delete_error}")
                
        time.sleep(5)
        driver.quit()
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from utils.helpers import get_current_time
from pages.categorycreation_page import CreateCategoryModal
from pages.categoryedition_page import EditCategoryModal


def create_category(driver, wait):

    category_page = CreateCategoryModal(driver, wait)
    category_page.open_clan_settings_menu()
    category_page.click_show_empty_categories()
    category_page.click_create_category_option()
    category_name = "Category " + get_current_time()
    category_page.input_category_name(category_name)
    time.sleep(0.5)
    category_page.click_confirm_create_category()   

    return category_name



def edit_category(driver, wait, old_category_name, new_category_name):
    category_page = EditCategoryModal(driver, wait)
    category_page.open_edit_menu(old_category_name)
    category_page.input_category_name(new_category_name)
    category_page.click_confirm_edit_category()
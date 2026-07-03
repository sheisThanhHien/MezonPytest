import time

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
    category_page.click_confirm_create_category()
    category_page.verify_category_created(category_name)

    return category_name



def edit_category(driver, wait, old_category_name, new_category_name):
    category_page = EditCategoryModal(driver, wait)
    
    category_page.open_category_context_menu(old_category_name)
    category_page.click_edit_category_option()
    time.sleep(1)
    category_page.input_category_name(new_category_name)
    time.sleep(1)
    category_page.click_save_changes_button()
    time.sleep(1)
    category_page.click_exit_category_edit_button()
    category_page.verify_category_name_displayed(new_category_name)

    return new_category_name
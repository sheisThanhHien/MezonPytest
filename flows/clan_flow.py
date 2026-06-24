from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages import clancreation_page
from pages.clancreation_page import CreateClanModal
from pages.clandeletion_page import DeleteClanModal


from utils.helpers import get_current_time


def create_clan(driver, wait):

    clancreation_page = CreateClanModal(driver, wait)
    clancreation_page.click_create_clan_button()
    clancreation_page.click_create_my_own_option()
    clan_name = "E2E Clan " + get_current_time()
    clancreation_page.input_clan_name(clan_name)
    clancreation_page.click_confirm_create_clan()
    clancreation_page.verify_clan_created(clan_name)
    return clan_name    
    


def delete_clan(driver, wait, clan_name):
    clandeletion_page = DeleteClanModal(driver, wait)
    clandeletion_page.open_clan_settings_menu()
    clandeletion_page.click_settings_menu_item()
    clandeletion_page.click_settings_sidebar_delete()
    clandeletion_page.input_delete_clan_name(clan_name)
    clandeletion_page.click_confirm_delete()

from pages.clancreation_page import CreateClanPage
from pages.clandeletion_page import DeleteClanPage
from utils.helpers import get_current_time


def create_clan(driver, wait):
    clan_page = CreateClanPage(driver, wait)
    clan_page.click_create_clan_button()
    clan_page.click_create_my_own_option()
    clan_name = "E2E Clan " + get_current_time()
    clan_page.input_clan_name(clan_name)
    clan_page.click_confirm_create_clan()
    clan_page.verify_clan_created(clan_name)
    return clan_name


def delete_clan(driver, wait, clan_name):
    clan_page = DeleteClanPage(driver, wait)
    clan_page.delete_clan(clan_name)
    clan_page.verify_clan_deleted(clan_name)

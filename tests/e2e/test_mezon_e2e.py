import pytest
from utils.helpers import get_current_time
from flows.auth_flow import login_email_password
from flows.clan_flow import create_clan, delete_clan
from flows.category_flow import create_category, edit_category
from flows.channel_flow import create_text_channel
from flows.message_flow import send_text_message



def _section(title):
    print(f"\n========== {title} ==========")


@pytest.mark.e2e
@pytest.mark.regression
def test_mezon_full_flow(driver, wait):
    _section("LOGIN")
    login_email_password(driver, wait)
    print("Login successfully!")

    _section("CREATE CLAN")
    clan_name = create_clan(driver, wait)
    print(f"Created clan: {clan_name}")
    print("✓ Clan verified")

    _section("CREATE CATEGORY")
    category_name = create_category(driver, wait)
    print(f"Created category: {category_name}")
    print("✓ Category verified")

    _section("EDIT CATEGORY")
    edited_category_name = "Category Edited " + get_current_time()
    edit_category(driver, wait, category_name, edited_category_name)
    print(f"Edited: {category_name} → {edited_category_name}")
    print("✓ Category edit verified")
    
    _section("CREATE TEXT CHANNEL")
    channel_name = create_text_channel(driver, wait, edited_category_name)
    print(f"Created channel: {channel_name} in category: {edited_category_name}")
    print("✓ Text channel verified")

    _section("SEND TEXT MESSAGE")
    message = send_text_message(driver, wait, channel_name)
    print(f"Sent message: {message}")
    print("✓ Message verified")

    _section("DELETE CLAN")
    delete_clan(driver, wait, clan_name)
    print(f"Deleted clan: {clan_name}")



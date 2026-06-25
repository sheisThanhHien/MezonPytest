# helpers.py
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from constants import BASE_URL, EMAIL, PASSWORD

import datetime

def get_current_time(): 
    return datetime.datetime.now().strftime("%Y%m%d %H%M%S")    

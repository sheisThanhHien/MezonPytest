# BASE_URL = "https://mezon.ai"
# URL Test Dev
BASE_URL = "https://dev-mezon.nccsoft.vn/"

# Account Test Prod
# EMAIL = "yocosa3965@crsay.com"
# PASSWORD = "Thanhhien312@"

# Account Test Dev
EMAIL = "yocosa3965@crsay.com"
PASSWORD = "Thanhhien312@"
INVALID_PASSWORD = PASSWORD + "@"


import datetime

def get_current_time(): 
    return datetime.datetime.now().strftime("%Y%m%d %H%M%S") 




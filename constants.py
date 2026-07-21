import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

BASE_URL = os.getenv("MEZON_BASE_URL", "https://dev-mezon.nccsoft.vn/")
EMAIL = os.getenv("MEZON_EMAIL", "hien.nguyenthanh+777@ncc.asia")
PASSWORD = os.getenv("MEZON_PASSWORD", "Autotest777@")

WAIT_TIMEOUT = int(os.getenv("MEZON_WAIT_TIMEOUT", "15"))
POLL_TIMEOUT = int(os.getenv("MEZON_POLL_TIMEOUT", "120"))
BROWSER_TEARDOWN_SLEEP = int(os.getenv("MEZON_BROWSER_TEARDOWN_SLEEP", "5"))

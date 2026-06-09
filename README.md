# Mezon Pytest — E2E Automation

End-to-end test suite for the [Mezon](https://mezon.ai) platform, built with **Selenium WebDriver** and **pytest**. The project simulates real user interactions in the browser: login, create/delete clans, manage categories, and send messages.

## Architecture

The project uses the **Page Object Model (POM)** combined with a **Flow layer**:

| Directory | Role |
|-----------|------|
| `pages/` | Defines locators and actions for each screen/modal |
| `flows/` | Groups business steps into reusable flows (login, create clan, create category, etc.) |
| `tests/` | Pytest test cases that call flows and assert results |
| `utils/` | Shared utilities (e.g. timestamp generation) |
| `constants.py` | URL, test account credentials, environment configuration |
| `conftest.py` | Pytest fixtures: Chrome driver setup and `WebDriverWait` |

```
Mezon_Pytest/
├── conftest.py
├── constants.py
├── requirements.txt
├── flows/
│   ├── auth_flow.py
│   ├── clan_flow.py
│   └── category_flow.py
├── pages/
│   ├── clancreation_page.py
│   ├── clandeletion_page.py
│   ├── categorycreation_page.py
│   └── categoryedition_page.py
├── tests/
│   ├── auth/
│   ├── clans/
│   ├── categories/
│   ├── channels/
│   └── e2e/
└── utils/
    └── helpers.py
```

## Requirements

- Python 3.8+
- Google Chrome
- [ChromeDriver](https://chromedriver.chromium.org/) compatible with your installed Chrome version (or use Selenium Manager built into Selenium 4.6+)

## Installation

```bash
# Clone the repository and navigate to the project directory
cd Mezon_Pytest

# Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `constants.py` before running tests:

```python
BASE_URL = "https://dev-mezon.nccsoft.vn/"   # Test environment URL
EMAIL = "your-test-email@example.com"
PASSWORD = "your-password"
INVALID_PASSWORD = PASSWORD + "@"            # Used for failed login tests
```

You can switch between **dev** and **production** environments by commenting/uncommenting the corresponding lines in this file.

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run by group
pytest tests/auth/
pytest tests/clans/
pytest tests/categories/
pytest tests/channels/
pytest tests/e2e/

# Run a specific file
pytest tests/e2e/test_mezon_e2e.py

# Run a specific test case
pytest tests/auth/test_login_success.py::test_mezon_login_success
```

## Test Suite

### Auth (`tests/auth/`)

| File | Description |
|------|-------------|
| `test_login_success.py` | Successful login with email and password |
| `test_login_failed.py` | Login with wrong password, verify error message |

### Clans (`tests/clans/`)

| File | Description |
|------|-------------|
| `test_create_clan.py` | Create a new clan and verify the name in the header |
| `test_delete_clan.py` | Delete a clan and verify it is removed from the sidebar |

### Categories (`tests/categories/`)

| File | Description |
|------|-------------|
| `test_create_category.py` | Create a category in a clan and verify it appears in the sidebar |
| `test_edit_category.py` | Rename a category and verify the new name |

### Channels (`tests/channels/`)

| File | Description |
|------|-------------|
| `test_send_message.py` | Send a message in a channel and verify it displays correctly |

### E2E (`tests/e2e/`)

| File | Description |
|------|-------------|
| `test_mezon_e2e.py` | Full flow: login → create clan → create category → edit category → delete clan |

## Core Flows

### Login (`flows/auth_flow.py`)

1. Open `BASE_URL`
2. Click **Login** → refresh the page
3. Select **Login with Email and Password**
4. Enter email, password, and submit

### Create / Delete Clan (`flows/clan_flow.py`)

- `create_clan()` — open the create clan modal, select "Create my own", enter a name (with timestamp), and confirm
- `delete_clan()` — open settings, delete the clan by re-entering the clan name

### Category Management (`flows/category_flow.py`)

- `create_category()` — enable empty categories display, create a new category
- `edit_category()` — open the category edit menu and rename it

## Fixtures

`conftest.py` provides two shared fixtures:

- **`driver`** — initializes `webdriver.Chrome()`, maximizes the window, and quits after the test finishes
- **`wait`** — `WebDriverWait(driver, 15)` with a 15-second timeout

Some tests (`test_login_failed`, `test_send_message`) manage their own driver instead of using the fixture.

## Notes

- Tests that create dynamic data (clans, categories) use timestamps via `get_current_time()` to avoid name collisions.
- Tests that create clans typically **clean up** with `delete_clan()` at the end.
- Locators prefer the `data-e2e` attribute for better stability than CSS classes.
- Error screenshots are saved to the `evidence/` directory (ignored in git).

## Dependencies

```
selenium
pytest
webdriver-manager
```

See [`requirements.txt`](requirements.txt) for details.

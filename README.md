# Mezon Pytest — E2E Automation

End-to-end test suite for the [Mezon](https://mezon.ai) platform, built with **Selenium WebDriver** and **pytest**.

## Architecture

The project uses **Page Object Model (POM)** + **Flow layer**:

| Directory | Role |
|-----------|------|
| `pages/` | Locators, UI actions, verify methods |
| `flows/` | Business steps reused by tests |
| `tests/` | Pytest cases — call flows only |
| `utils/` | Shared helpers |
| `constants.py` | Environment config (URL, credentials, timeouts) |
| `conftest.py` | Shared fixtures, screenshot on failure, e2e report |

```
Mezon_Pytest/
├── conftest.py
├── constants.py
├── .env.example
├── flows/
│   ├── auth_flow.py
│   ├── clan_flow.py
│   ├── category_flow.py
│   ├── channel_flow.py
│   ├── message_flow.py
│   └── thread_flow.py
├── pages/
│   ├── base_page.py
│   ├── auth_page.py
│   ├── clan_header_page.py
│   ├── clancreation_page.py
│   ├── clandeletion_page.py
│   ├── categorycreation_page.py
│   ├── categoryedition_page.py
│   ├── channel_page.py
│   ├── message_page.py
│   ├── thread_base_page.py
│   ├── thread_from_message_page.py
│   └── thread_list_page.py
└── tests/
    ├── auth/
    ├── clans/
    ├── categories/
    ├── channels/
    ├── messages/
    ├── threads/
    └── e2e/
```

## Conventions

1. **Page** — locator + action + verify UI
2. **Flow** — ghép bước nghiệp vụ, gọi verify từ page
3. **Test** — chỉ gọi flow, không lặp verify
4. **Locator** — ưu tiên `data-e2e`
5. **Menu clan** — click theo label text (`"Clan Settings"`, `"Create Category"`), không dùng index

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # chỉnh credential tại đây
```

## Configuration

Biến môi trường (hoặc file `.env`):

| Variable | Description |
|----------|-------------|
| `MEZON_BASE_URL` | Test environment URL |
| `MEZON_EMAIL` | Test account email |
| `MEZON_PASSWORD` | Test account password |
| `MEZON_WAIT_TIMEOUT` | WebDriverWait timeout (default: 15) |
| `MEZON_POLL_TIMEOUT` | Poll verify timeout (default: 120) |

## Running Tests

```bash
pytest                          # all tests
pytest tests/clans/ -v -s
pytest tests/threads/ -v -s
pytest tests/e2e/ -m e2e -v -s
```

## Test Groups

| Marker | Directory |
|--------|-----------|
| `auth` | `tests/auth/` |
| `clans` | `tests/clans/` |
| `categories` | `tests/categories/` |
| `channels` | `tests/channels/` |
| `messages` | `tests/messages/` |
| `threads` | `tests/threads/` |
| `e2e` | `tests/e2e/` |

## Notes

- Dynamic test data dùng timestamp qua `utils.helpers.get_current_time()`
- Screenshot tự động lưu vào `evidence/` khi test fail
- E2E report HTML/JSON khi chạy với `-m e2e`

import time
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from constants import (
    BROWSER_TEARDOWN_SLEEP,
    HEADLESS,
    TEST_RERUNS,
    TEST_RERUNS_DELAY,
    WAIT_TIMEOUT,
)
from utils.e2e_report import E2EReport


def _is_e2e_run(config):
    markexpr = config.getoption("markexpr") or ""
    return "e2e" in markexpr


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome headless (no visible browser window)",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Chrome with visible browser window (overrides --headless and MEZON_HEADLESS)",
    )


def _is_headless(config):
    if config.getoption("--headed"):
        return False
    if config.getoption("--headless"):
        return True
    return HEADLESS


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    reruns_option = getattr(config.option, "reruns", 0)
    if reruns_option == 0 and TEST_RERUNS > 0:
        config.option.reruns = TEST_RERUNS
        config.option.reruns_delay = TEST_RERUNS_DELAY

    if _is_e2e_run(config):
        E2EReport.start()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        evidence_dir = Path("evidence")
        evidence_dir.mkdir(exist_ok=True)
        screenshot_name = f"failure_{item.name}.png"
        screenshot_path = evidence_dir / screenshot_name
        png = driver.get_screenshot_as_png()
        screenshot_path.write_bytes(png)
        allure.attach(
            png,
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    if not E2EReport.has_steps():
        return

    report_paths = E2EReport.write_reports(exitstatus)
    terminal = session.config.pluginmanager.get_plugin("terminalreporter")
    if terminal:
        terminal.write_line(
            f"\nOpen E2E report: {report_paths['html']}",
            yellow=True,
        )
        terminal.write_line(
            f"E2E JSON report: {report_paths['json']}",
            yellow=True,
        )


@pytest.fixture
def driver(request):
    options = Options()
    headless = _is_headless(request.config)
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    if not headless:
        driver.maximize_window()
    yield driver

    time.sleep(BROWSER_TEARDOWN_SLEEP)
    driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, WAIT_TIMEOUT)

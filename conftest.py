import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from constants import BROWSER_TEARDOWN_SLEEP, WAIT_TIMEOUT
from utils.e2e_report import E2EReport


def _is_e2e_run(config):
    markexpr = config.getoption("markexpr") or ""
    return "e2e" in markexpr


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
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
        screenshot_path = evidence_dir / f"failure_{item.name}.png"
        driver.save_screenshot(str(screenshot_path))
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
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver

    time.sleep(BROWSER_TEARDOWN_SLEEP)
    driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, WAIT_TIMEOUT)

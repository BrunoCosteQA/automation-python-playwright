import pytest
from playwright.sync_api import Error, sync_playwright
from pytest_html import extras as html_extras

from core.screenshot_service import ScreenshotService

BASE_URL = "https://exemplo-seu-sistema.com"


# ---------------- FIXTURES PLAYWRIGHT ----------------

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    try:
        browser = playwright_instance.chromium.launch(headless=True)
    except Error as exc:  # navegadores Playwright ausentes
        pytest.skip(
            "Playwright browsers não encontrados. Execute 'playwright install' antes de rodar os testes.",
            allow_module_level=True,
        )
        raise exc

    yield browser
    browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


# ---------------- FIXTURES DE CONFIG / SERVICE ----------------

@pytest.fixture(scope="session")
def screenshot_service():
    return ScreenshotService(base_dir="evidencias")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


# ---------------- HOOK pytest-html (opcional) ----------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Anexa screenshot ao pytest-html somente se:
       - teste falhar
       - e pytest-html estiver ativo (usuário passou --html)
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        screenshot_service = item.funcargs.get("screenshot_service")

        if page and screenshot_service:
            safe_name = report.nodeid.replace("::", "_").replace("/", "_")

            worker_id = "local"
            if hasattr(item.config, "workerinput"):
                worker_id = item.config.workerinput.get("workerid", "local")

            name_prefix = f"{safe_name}_{worker_id}"
            screenshot_path = screenshot_service.save(page, name_prefix=name_prefix)

            if screenshot_path is not None:
                extra = getattr(report, "extra", [])
                extra.append(html_extras.image(str(screenshot_path), mime_type="image/png"))
                report.extra = extra


def pytest_html_report_title(report):
    report.title = "Relatório Frontend - Qualidade é Estratégia"

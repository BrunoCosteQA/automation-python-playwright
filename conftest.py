import pytest
from playwright.sync_api import Error, sync_playwright
from pytest_html import extras as html_extras
from core.screenshot_service import ScreenshotService


ENV_URLS = {
    "dev": "https://www.google.com",
    "hml": "https://www.google.com",
    "prod": "https://www.google.com",
}


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Ambiente alvo (dev, hml, prod). Pode ser usado para definir URLs específicas.",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="URL base personalizada. Se informada, tem prioridade sobre o mapeamento por ambiente.",
    )


# ---------------- FIXTURES PLAYWRIGHT ----------------

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    try:
        browser = playwright_instance.chromium.launch(headless=False)
    except Error as exc:  # navegadores Playwright ausentes
        pytest.skip(
            "Playwright browsers não encontrados. Execute 'playwright install' antes de rodar os testes.",
            allow_module_level=True,
        )
        raise exc

    yield browser
    browser.close()


@pytest.fixture
def context(browser, base_url):
    context = browser.new_context(base_url=base_url)
    try:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    except Exception:
        pass
    yield context
    try:
        context.tracing.stop()
    except Exception:
        pass
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    console_messages = []

    def _on_console(message):
        console_messages.append(f"[{message.type}] {message.text}")

    page.on("console", _on_console)
    page.console_messages = console_messages  # type: ignore[attr-defined]
    yield page


# ---------------- FIXTURES DE CONFIG / SERVICE ----------------

@pytest.fixture(scope="session")
def screenshot_service():
    return ScreenshotService(base_dir="evidencias")


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    custom_url = pytestconfig.getoption("--base-url")
    if custom_url:
        return custom_url

    env = pytestconfig.getoption("--env").lower()
    if env not in ENV_URLS:
        raise pytest.UsageError(
            f"Ambiente '{env}' não suportado. Use um de: {', '.join(ENV_URLS.keys())}."
        )

    return ENV_URLS[env]


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
        context = item.funcargs.get("context")

        if page and screenshot_service:
            safe_name = report.nodeid.replace("::", "_").replace("/", "_")

            worker_id = "local"
            if hasattr(item.config, "workerinput"):
                worker_id = item.config.workerinput.get("workerid", "local")

            name_prefix = f"{safe_name}_{worker_id}"
            screenshot_path = screenshot_service.save(page, name_prefix=name_prefix)
            console_path = screenshot_service.save_console_logs(
                getattr(page, "console_messages", []), name_prefix=name_prefix
            )
            trace_path = (
                screenshot_service.export_trace(context, name_prefix=name_prefix)
                if context
                else None
            )

            extra = getattr(report, "extra", [])
            if screenshot_path is not None:
                extra.append(html_extras.image(str(screenshot_path), mime_type="image/png"))
            if console_path:
                extra.append(
                    html_extras.html(
                        f'<a href="file://{console_path}" target="_blank">Console logs</a>'
                    )
                )
            if trace_path:
                extra.append(
                    html_extras.html(
                        f'<a href="file://{trace_path}" target="_blank">Playwright trace</a>'
                    )
                )

            if extra:
                report.extra = extra


def pytest_html_report_title(report):
    report.title = "Relatório"

from typing import Optional
from playwright.sync_api import Page, expect

from core.screenshot_service import ScreenshotService


class BasePage:
    def __init__(self, page: Page, screenshot_service: Optional[ScreenshotService] = None):
        self.page = page
        self.screenshot_service = screenshot_service

    # ----------------- Ações de Página -----------------

    def open(self, url: str):
        self.page.goto(url)

    def click(self, locator: str):
        self.page.locator(locator).click()

    def fill(self, locator: str, text: str):
        self.page.locator(locator).fill(text)

    # ----------------- Validações -----------------------

    def should_see_text(self, text: str, screenshot_on_fail: bool = False):
        """
        Valida se um texto está visível na página.
        Se falhar e screenshot_on_fail=True:
        - Usa ScreenshotService para evidência.
        """
        try:
            expect(self.page.get_by_text(text)).to_be_visible()
        except AssertionError:
            if screenshot_on_fail and self.screenshot_service:
                self.screenshot_service.save(self.page, f"erro_should_see_{text}")
            raise

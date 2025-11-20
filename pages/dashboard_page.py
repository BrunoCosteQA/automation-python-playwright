from typing import Optional

from playwright.sync_api import Page

from core.base_page import BasePage
from core.screenshot_service import ScreenshotService


class DashboardPage(BasePage):
    """Representa o dashboard autenticado e suas ações de navegação."""

    def __init__(self, page: Page, screenshot_service: Optional[ScreenshotService] = None):
        """Configura os elementos principais do dashboard reutilizados nos fluxos.

        Args:
            page: Instância sincronizada do Playwright utilizada nos fluxos do dashboard.
            screenshot_service: Serviço opcional para registrar evidências.
        """
        super().__init__(page, screenshot_service)
        self.sidebar_menu = page.get_by_role("navigation")
        self.user_menu_button = page.get_by_role("button", name="Menu do usuário")
        self.logout_option = page.get_by_role("link", name="Sair")
        self.modal_dialog = page.get_by_role("dialog")
        self.modal_confirm_button = self.modal_dialog.get_by_role("button", name="Confirmar")
        self.modal_cancel_button = self.modal_dialog.get_by_role("button", name="Cancelar")
        self.page_title = page.get_by_role("heading")

    def abrir(self, base_url: str):
        """Acessa o dashboard a partir da base_url e valida o fragmento da URL.

        Args:
            base_url: Endereço raiz da aplicação, usado para montar a URL do dashboard.
        """
        self.open(f"{base_url}/dashboard")
        self.expect_url_contains("dashboard")

    def acessar_modulo(self, nome_modulo: str):
        """Clica no módulo desejado na barra lateral e confirma a navegação pelo URL.

        Args:
            nome_modulo: Rótulo do módulo exibido no menu lateral.
        """
        self.click(self.sidebar_menu.get_by_role("link", name=nome_modulo))
        self.expect_url_contains(nome_modulo.lower())

    def abrir_menu_usuario(self):
        """Expande o menu do usuário e aguarda as opções ficarem visíveis."""
        self.click(self.user_menu_button)
        self.expect_visible(self.logout_option)

    def logout(self):
        """Realiza logout abrindo o menu do usuário e clicando em "Sair"."""
        self.abrir_menu_usuario()
        self.click(self.logout_option)

    def confirmar_modal(self):
        """Confirma um modal genérico aguardando visibilidade e ocultamento após a ação."""
        self.wait_for_locator(self.modal_dialog)
        self.click(self.modal_confirm_button)
        self.expect_hidden(self.modal_dialog)

    def cancelar_modal(self):
        """Cancela um modal genérico aguardando visibilidade e desaparecimento posterior."""
        self.wait_for_locator(self.modal_dialog)
        self.click(self.modal_cancel_button)
        self.expect_hidden(self.modal_dialog)

    def validar_titulo(self, titulo: str):
        """Verifica título da aba e heading principal exibidos no dashboard."""
        self.expect_title_contains(titulo)
        self.expect_text_contains(self.page_title, titulo)

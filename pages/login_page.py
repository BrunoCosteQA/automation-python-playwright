from typing import Optional

from playwright.sync_api import Page

from core.base_page import BasePage
from core.screenshot_service import ScreenshotService


class LoginPage(BasePage):
    """Modela a tela de autenticação com seletores centrais reutilizáveis."""

    def __init__(self, page: Page, screenshot_service: Optional[ScreenshotService] = None):
        """Inicializa a página de login e resolve os seletores reutilizados nos cenários.

        Args:
            page: Instância sincronizada do Playwright utilizada na navegação.
            screenshot_service: Serviço opcional para evidências em falhas.
        """
        super().__init__(page, screenshot_service)
        self.usuario_input = page.locator("input[name=\"usuario\"]")
        self.senha_input = page.locator("input[name=\"senha\"]")
        self.submit_button = page.locator("button[type=\"submit\"]")
        self.login_heading = page.get_by_role("heading", name="Fazer Login")

    def abrir(self, base_url: str):
        """Navega para a URL base exibindo a tela de login.

        Args:
            base_url: Endereço raiz configurado para a aplicação.
        """
        self.open(base_url)

    def realizar_login(self, usuario: str, senha: str):
        """Preenche as credenciais e aciona o envio do formulário de login.

        Args:
            usuario: Nome de usuário válido para autenticação.
            senha: Senha correspondente ao usuário informado.
        """
        self.wait_for_locator(self.usuario_input)
        self.fill(self.usuario_input, usuario)
        self.fill(self.senha_input, senha)
        self.click(self.submit_button)

    def validar_tela_login(self):
        """Garante que o heading principal de login está visível para o usuário."""
        self.expect_visible(self.login_heading)

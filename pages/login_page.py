from typing import Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
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
        self.fazer_login_click = page.locator("//a[@aria-label='Fazer login']")
        self.usuario_input = page.get_by_role("textbox", name="E-mail ou telefone")
        self.avancar_button = page.get_by_role("button", name="Avançar")
        self.criar_conta_button = page.locator("//button[.//span[text()='Criar conta']]")
        self.uso_pessoal_button = page.locator("//li[.//span[text()='Para uso pessoal']]")
        self.senha_input = page.get_by_label("Senha", exact=False)
        self.submit_button = page.get_by_role("button", name="Próxima")

    def abrir(self, base_url: str):
        """Navega para a URL base exibindo a tela de login.

        Args:
            base_url: Endereço raiz configurado para a aplicação.
        """
        self.open(base_url)
        self.click(self.fazer_login_click)

    def criar_conta(self):
        """Preenche as credenciais e aciona o envio do formulário de login.
        """
        self.click(self.criar_conta_button, wait_before_ms=3000)
        self.click(self.uso_pessoal_button)

    def realizar_login(self, usuario: str, senha: str):
        """Preenche as credenciais e aciona o envio do formulário de login.

        Args:
            usuario: Nome de usuário válido para autenticação.
            senha: Senha correspondente ao usuário informado.
        """
        self.wait_for_locator(self.usuario_input)
        self.fill(self.usuario_input, usuario)
        self.click(self.avancar_button)
        self.fill(self.senha_input, senha)
        self.click(self.submit_button)

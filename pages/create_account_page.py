from typing import Optional
from playwright.sync_api import Page
from core.base_page import BasePage
from core.screenshot_service import ScreenshotService


class CreateAccountPage(BasePage):
    """Modela a tela de autenticação com seletores centrais reutilizáveis."""

    def __init__(self, page: Page, screenshot_service: Optional[ScreenshotService] = None):
        """Inicializa a página de login e resolve os seletores reutilizados nos cenários.

        Args:
            page: Instância sincronizada do Playwright utilizada na navegação.
            screenshot_service: Serviço opcional para evidências em falhas.
        """
        super().__init__(page, screenshot_service)
        self.nome_input = page.locator("input[id='firstName']")
        self.sobrenome_input = page.locator("input[id='lastName']")
        self.avancar_button = page.locator("//button[.//span[text()='Avançar']]")
        self.dia_input = page.locator("input[id='day']")
        self.mes_box = page.locator("//*[@id='month']")
        self.ano_input = page.locator("input[id='year']")
        self.genero_box = page.locator("//div[@role='combobox'][.//span[normalize-space()='Gênero']]")
        self.email_sugestao_text = page.locator("//div[@id='selectionc22']")
        self.crie_email_radio = page.locator("//input[@aria-labelledby='selectionc22']")
        self.nome_email = page.locator("input[name='Username']")
        self.senha_input = page.locator("input[name='Passwd']")
        self.senha_confirmar_input = page.locator("input[name='PasswdAgain']")
        self.confirme_informacoes_text = page.locator("//span[contains(text(), 'Confirme algumas')]")

    def inserir_nome_sobrenome(self, nome: str, sobrenome: str):
        """Preenche nome e sobrenome na criação de conta.

        Args:
            nome: Nome de usuário válido para autenticação.
            sobrenome: Nome de usuário válido para autenticação.
        """
        self.fill(self.nome_input, nome)
        self.fill(self.sobrenome_input, sobrenome)
        self.click(self.avancar_button)

    def inserir_infos_basicas(self, dia: str, mes: str, ano: str, genero: str):
        """Preenche Data de Nascimento e Genero na criação de conta.

        Args:
            dia: dia de nascimento.
            mes: mes de nascimento (Ex: Janeiro, Fevereiro, Março).
            ano: ano de nascimento
            genero: tipo de genero (Ex: Mulher, Homem, Prefiro não dizer).
        """
        locator_mes = f"//li[.//span[normalize-space()='{mes}']]"
        locator_genero = f"//ul[@role='listbox' and @aria-label='Gênero']//li[.//span[normalize-space()='{genero}']]"

        self.fill(self.dia_input, dia)
        self.click_and_select(self.mes_box,option_locator= locator_mes)
        self.fill(self.ano_input, ano)
        self.click_and_select(self.genero_box,option_locator=locator_genero)
        self.click(self.avancar_button)

    def inserir_username(self, username: str):
        """Preenche username na criação de conta.

        Args:
            username: Nome de usuário válido para o email.
        """
        if self.is_visible(self.email_sugestao_text):
            self.click(self.crie_email_radio)
        self.fill(self.nome_email, username)
        self.click(self.avancar_button)

    def inserir_senha(self, senha: str):
        """Preenche senha na criação de conta.

        Args:
            senha: Senha válida para o email.
        """
        self.fill(self.senha_input, senha)
        self.fill(self.senha_confirmar_input, senha)
        self.click(self.avancar_button)
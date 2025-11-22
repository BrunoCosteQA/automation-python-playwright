from typing import Optional

from playwright.sync_api import Page

from core.base_page import BasePage
from core.screenshot_service import ScreenshotService


class CreateAccountPage(BasePage):
    """Modela o fluxo de criação de conta do Google."""

    def __init__(self, page: Page, screenshot_service: Optional[ScreenshotService] = None):
        """Inicializa a página de criação de conta e resolve os seletores principais.

        Args:
            page: Instância sincronizada do Playwright utilizada na navegação.
            screenshot_service: Serviço opcional para evidências em falhas.
        """
        super().__init__(page, screenshot_service)
        self.nome_input = page.get_by_label("Nome", exact=True)
        self.sobrenome_input = page.locator("input[id='lastName']")
        self.avancar_button = page.get_by_role("button", name="Avançar")
        self.dia_input = page.locator("input[id='day']")
        self.mes_box = page.locator("//*[@id='month']")
        self.ano_input = page.locator("input[id='year']")
        self.genero_box = page.locator("//div[@role='combobox'][.//span[normalize-space()='Gênero']]")
        self.email_sugestao_text = page.get_by_role("radio", name="Crie seu próprio endereço do Gmail")
        self.email_sugestao_radio = page.locator("//input[@type='radio'][@aria-labelledby='selectionc22']")
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
        """Preenche data de nascimento e gênero na criação de conta.

        Args:
            dia: Dia de nascimento.
            mes: Mês de nascimento (Ex: Janeiro, Fevereiro, Março).
            ano: Ano de nascimento.
            genero: Tipo de gênero (Ex: Mulher, Homem, Prefiro não dizer).
        """
        locator_mes = f"//li[.//span[normalize-space()='{mes}']]"
        locator_genero = f"//ul[@role='listbox' and @aria-label='Gênero']//li[.//span[normalize-space()='{genero}']]"

        self.fill(self.dia_input, dia)
        self.click_and_select(self.mes_box, option_locator=locator_mes)
        self.fill(self.ano_input, ano)
        self.click_and_select(self.genero_box, option_locator=locator_genero)
        self.click(self.avancar_button)

    def inserir_username(self, username: str):
        """Preenche username na criação de conta.

        Args:
            username: Nome de usuário válido para o email.
        """
        if self.exists(self.email_sugestao_text, timeout=5000):
            self.click(self.email_sugestao_radio)
        self.fill(self.nome_email, username)
        self.click(self.avancar_button)

    def inserir_senha(self, senha: str):
        """Preenche senha e confirmação na criação de conta.

        Args:
            senha: Senha válida para o email.
        """
        self.fill(self.senha_input, senha)
        self.fill(self.senha_confirmar_input, senha)
        self.click(self.avancar_button)

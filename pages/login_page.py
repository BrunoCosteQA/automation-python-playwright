from core.base_page import BasePage


class LoginPage(BasePage):

    def abrir(self, base_url: str):
        self.open(base_url)

    def realizar_login(self, usuario: str, senha: str):
        self.fill('input[name="usuario"]', usuario)
        self.fill('input[name="senha"]', senha)
        self.click('button[type="submit"]')

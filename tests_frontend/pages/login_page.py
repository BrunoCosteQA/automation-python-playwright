from core.base_page import BasePage


class LoginPage(BasePage):

    PATH = "/login"

    def abrir(self, base_url: str):
        self.open(base_url + self.PATH)

    def realizar_login(self, usuario: str, senha: str):
        self.fill('input[name="usuario"]', usuario)
        self.fill('input[name="senha"]', senha)
        self.click('button[type="submit"]')

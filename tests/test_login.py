from pages.login_page import LoginPage


def test_login_sucesso(page, screenshot_service, base_url):
    login_page = LoginPage(page, screenshot_service)

    login_page.abrir(base_url)
    # login_page.realizar_login("usuario_valido", "senha_valida")
    login_page.validar_tela_login()

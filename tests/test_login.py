from pages.login_page import LoginPage


def test_login_sucesso(page, screenshot_service, base_url):
    login_page = LoginPage(page, screenshot_service)

    login_page.abrir(base_url)
    print('acessou area login')
    login_page.realizar_login("thrashers.013@gmail.com", "senha_valida")

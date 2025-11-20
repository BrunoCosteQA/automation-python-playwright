from pages.create_account_page import CreateAccountPage
from pages.login_page import LoginPage
from util import generate_data


def test_created_account_sucesso(page, screenshot_service, base_url):
    # Dado que eu esteja na tela de Criação de Conta
    login_page = LoginPage(page, screenshot_service)
    login_page.abrir(base_url)
    login_page.criar_conta()

    # Quando preencho as informações para criação de conta
    created_account_page = CreateAccountPage(page, screenshot_service)
    created_account_page.inserir_nome_sobrenome("Bruno", "Teste")
    created_account_page.inserir_infos_basicas('20', 'Agosto', '1992', 'Homem')
    created_account_page.inserir_username(f'email.{generate_data.generate_random_code()}')
    created_account_page.inserir_senha('SenhaPadr@0Google')

    # Então exibe o QRCODE para finalizar o processo pelo celular
    text_confirmacao_conta = 'Confirme algumas informações antes de criar uma conta'
    created_account_page.expect_text(created_account_page.confirme_informacoes_text, text_confirmacao_conta)




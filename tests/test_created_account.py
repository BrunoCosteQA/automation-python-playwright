from pages.create_account_page import CreateAccountPage
from pages.login_page import LoginPage
from util.user_builder import UserBuilder


def test_created_account_sucesso(page, screenshot_service, base_url):
    # Dados dinâmicos do usuário
    user = UserBuilder.build(genero="Homem")

    # Dado que eu esteja na tela de Criação de Conta
    login_page = LoginPage(page, screenshot_service)
    login_page.abrir(base_url)
    login_page.criar_conta()

    # Quando preencho as informações para criação de conta
    created_account_page = CreateAccountPage(page, screenshot_service)
    created_account_page.inserir_nome_sobrenome(user.nome, user.sobrenome)
    created_account_page.inserir_infos_basicas(user.dia, user.mes, user.ano, user.genero)
    created_account_page.inserir_username(user.email)
    created_account_page.inserir_senha(user.senha)

    # Então exibe o QRCODE para finalizar o processo pelo celular
    texto_confirmacao = 'Confirme algumas informações antes de criar uma conta'
    created_account_page.expect_text(created_account_page.confirme_informacoes_text, texto_confirmacao)

# Automação Web com Playwright + Pytest

Projeto modelo para criar e validar fluxos web usando **Playwright** (API síncrona) e **Pytest**. O código segue a organização recomendada na [documentação oficial do Playwright](https://playwright.dev/python/docs/intro) para criação de fixtures reutilizáveis, uso de `base_url` e geração de evidências (tracing/screenshot/console).

## Visão geral
- **Page Objects enxutos** em `pages/` estendem `BasePage`, que encapsula helpers de clique, preenchimento, asserts e waits explícitos (`Locator.wait_for`, `expect`).
- **Fixtures de sessão** em `conftest.py` criam `browser`, `context` e `page` conforme o modelo dos exemplos oficiais, permitindo configurar `base_url`, headless/headed e tracing.
- **Evidências automáticas** via `ScreenshotService`, anexando screenshots, logs e traces ao `pytest-html` apenas em falhas.
- **Geração de dados** com Faker para construir usuários dinâmicos nos cenários de teste.

## Estrutura do projeto
```
core/
├─ base_page.py            # Ações e asserts genéricos para páginas
└─ screenshot_service.py   # Serviço opcional de evidências (screenshot, console, trace)
pages/
├─ login_page.py           # Fluxo de autenticação e acesso ao cadastro
└─ create_account_page.py  # Formulário de criação de conta Google
util/
├─ faker_data.py           # Factory do Faker pt_BR
└─ user_builder.py         # Builder de usuários com dados dinâmicos
conftest.py                # Fixtures Playwright + hooks do pytest-html
pytest.ini                 # Configuração padrão do Pytest
requirements.txt           # Dependências do projeto
run_local.sh               # Atalho para execução local com HTML report
```

## Pré-requisitos
- Python 3.10+
- Dependências do `requirements.txt`
- Navegadores Playwright instalados (`playwright install`), conforme [guia oficial](https://playwright.dev/python/docs/browsers#install-browsers).

Instalação recomendada:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Execução dos testes
Execução padrão (headless true por padrão, seguindo o comportamento oficial do Playwright):
```bash
pytest
```

Gerar relatório HTML com evidências automáticas:
```bash
./run_local.sh
```
O script apenas adiciona `--html=reports/report.html --self-contained-html`; as evidências de falha são anexadas pelo hook `pytest_runtest_makereport`.

### Configuração de ambiente/base URL
- Selecionar um ambiente predefinido: `pytest --env=hml`
- Informar uma URL customizada (prioritária): `pytest --base-url=https://minha-url.com`
- Forçar execução visível: `HEADLESS=false pytest`

O `base_url` é injetado no contexto Playwright e permite usar caminhos relativos nos Page Objects, como recomendado em [Base URLs](https://playwright.dev/python/docs/api/class-browsercontext#browser-context-new-page-option-base-url).

## Fluxo coberto
O teste `tests/test_created_account.py` percorre o fluxo de criação de conta Google:
1. Abre a home do Google e aciona **Fazer login**.
2. Escolhe **Criar conta > Para uso pessoal**.
3. Preenche dados pessoais, data de nascimento, gênero, username e senha.
4. Valida o texto de confirmação antes do QR Code.

## Evidências e tracing
- **Screenshots**: salvos em `evidencias/YYYY-MM-DD/` com nome único; respeitam `DISABLE_SCREENSHOTS=1`.
- **Logs de console**: capturados via listener `page.on("console")` e anexados ao report.
- **Tracing**: iniciado em cada contexto com `context.tracing.start` (screenshots/snapshots/sources) e exportado apenas em falhas, alinhado ao [guia de tracing](https://playwright.dev/python/docs/trace-viewer).

## Diagrama de classes
Consulte o diagrama em [`docs/class_diagram.md`](docs/class_diagram.md) para visualizar as relações entre Page Objects, serviços e utilitários.

## Dicas adicionais
- Mantenha seletores legíveis usando `get_by_role`/`get_by_label` quando possível, conforme as [melhores práticas de acessibilidade](https://playwright.dev/python/docs/locators#locate-by-role).
- Prefira os helpers de `BasePage` (`click`, `fill`, `expect_*`) para manter asserções e waits consistentes.
- Para paralelismo, os nomes de screenshot incluem `workerid`, evitando colisões em múltiplos workers do pytest-xdist.

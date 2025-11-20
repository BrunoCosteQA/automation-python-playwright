# Automação Web com Playwright + Pytest

Template mínimo para criar e validar fluxos web usando **Playwright** (API síncrona) e **Pytest**. O projeto adota Page Objects enxutos, serviços reutilizáveis e fixtures de sessão para facilitar execução local ou em pipeline.

## Estrutura do projeto
```
core/
├─ base_page.py            # Ações e asserts genéricos para páginas
└─ screenshot_service.py   # Serviço opcional de evidências (screenshot, console, trace)
pages/
├─ login_page.py           # Fluxo de autenticação e navegação para criação de conta
└─ create_account_page.py  # Formulário de criação de conta Google
util/
└─ generate_data.py        # Geração de strings aleatórias/UUIDs
conftest.py                # Fixtures Playwright + hooks do pytest-html
pytest.ini                 # Configuração padrão do Pytest
requirements.txt           # Dependências do projeto
run_local.sh               # Atalho para execução local com HTML report
``` 

## Pré-requisitos
- Python 3.10+
- Navegadores Playwright instalados

Instale dependências e navegadores:
```bash
pip install -r requirements.txt
playwright install
```

## Execução dos testes
Com a configuração padrão (sem HTML):
```bash
pytest
```

Gerar relatório HTML localmente:
```bash
./run_local.sh
```

### Configuração de ambiente/base URL
- Selecione um ambiente predefinido: `pytest --env=hml`
- Forneça uma URL customizada (tem prioridade): `pytest --base-url=https://minha-url.com`

Mapeamento padrão (`conftest.py`): dev/hml/prod apontam para `https://www.google.com`. O `base_url` é injetado no contexto Playwright, permitindo usar caminhos relativos nas páginas.

## Classes e serviços principais
- **BasePage (`core/base_page.py`)**: helper para abrir URLs, clicar, preencher campos, aguardar estados de `Locator` e validar texto/URL/título. Inclui utilitários booleanos (`is_visible`, `is_hidden`) e suporte opcional a screenshots em falhas via `ScreenshotService`.
- **ScreenshotService (`core/screenshot_service.py`)**: salva evidências em `evidencias/<YYYY-MM-DD>/` com nomes únicos. Respeita `DISABLE_SCREENSHOTS=1` e pode exportar logs de console e traces Playwright quando habilitados.
- **LoginPage (`pages/login_page.py`)**: modela a tela de login do Google, abrindo a página inicial, acionando “Fazer login” e permitindo iniciar o fluxo de criação de conta ou realizar login com usuário/senha.
- **CreateAccountPage (`pages/create_account_page.py`)**: cobre o formulário de criação de conta (nome, data de nascimento/gênero, username, senha) usando seletores dinâmicos para listas suspensas.
- **Geração de dados (`util/generate_data.py`)**: produz UUIDs e strings aleatórias para evitar colisões em testes de criação de conta.

## Hooks e evidências
O hook `pytest_runtest_makereport` anexa screenshots, logs de console e traces ao HTML report apenas quando os testes falham e o Pytest é executado com `--html`. A nomeação inclui `workerid` para evitar colisões em execuções paralelas.

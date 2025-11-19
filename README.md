# Testes de Frontend com Playwright + Pytest

Este repositório fornece um template enxuto para automação web com **Playwright** e **Pytest**, seguindo os princípios de Page Objects leves, serviços desacoplados e execução segura em pipeline.

## Estrutura
```
tests_frontend/
├─ core/
│  ├─ base_page.py
│  └─ screenshot_service.py
├─ pages/
│  └─ login_page.py
├─ tests/
│  └─ test_login.py
├─ conftest.py
├─ requirements.txt
├─ pytest.ini
└─ run_local.sh        # opcional (gera HTML apenas localmente)
```

## Pré-requisitos
- Python 3.10+
- Navegadores Playwright instalados

Instalação das dependências e navegadores:
```bash
pip install -r tests_frontend/requirements.txt
playwright install
```

## Execução
Por padrão a pipeline não gera relatório HTML. Para rodar os testes com a configuração padrão:
```bash
cd tests_frontend
pytest
```

Para gerar relatório HTML localmente use o script auxiliar:
```bash
cd tests_frontend
./run_local.sh
```

### Dica rápida (erro de browser ausente)
Se o Pytest pular os testes com a mensagem:
```
Playwright browsers não encontrados. Execute 'playwright install' antes de rodar os testes.
```
basta rodar o comando `playwright install` para baixar os navegadores necessários.

## Screenshots
- Salvos automaticamente em `evidencias/<YYYY-MM-DD>/` quando `screenshot_on_fail=True` nas asserções ou via hook do pytest-html.
- Para desabilitar (por exemplo, em pipeline), defina `DISABLE_SCREENSHOTS=1` no ambiente.

## Paralelismo
A geração de screenshots usa timestamp + UUID para evitar colisões em execuções com `pytest-xdist`.

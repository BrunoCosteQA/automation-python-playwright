import re
import logging
from typing import Literal, Optional, Union
from playwright.sync_api import Locator, Page, expect
from core.screenshot_service import ScreenshotService

logger = logging.getLogger(__name__)
Locatable = Union[str, Locator]


class BasePage:
    """Camada base para páginas, encapsulando waits, asserts e serviços auxiliares."""

    def __init__(self, page: Page, screenshot_service: Optional[ScreenshotService] = None):
        """Guarda a instância de página e o serviço de screenshot para reutilização em helpers.

        Args:
            page: Instância sincronizada do Playwright utilizada pela página.
            screenshot_service: Serviço opcional para captura de screenshots em falhas.
        """
        self.page = page
        self.screenshot_service = screenshot_service

    def _resolve_locator(self, target: Locatable) -> Locator:
        """Converte strings em Locator Playwright mantendo a flexibilidade de assinatura.

        Args:
            target: Seletor CSS/XPath ou locator já resolvido.

        Returns:
            Locator correspondente ao alvo informado.
        """
        return self.page.locator(target) if isinstance(target, str) else target

    # ----------------- Ações de Página -----------------

    def open(self, url: str):
        """Abre uma URL absoluta usando o navegador controlado pelo Playwright."""
        self.page.goto(url)

    def click(self, locator: Locatable):
        """Realiza clique em um locator já resolvido ou seletor CSS/XPath.

        Args:
            locator: Seletor de string ou locator Playwright para clique.
        """
        self._resolve_locator(locator).click()

    def click_and_select(self, box_locator: Locatable, option_locator: Locatable):
        """Abre um seletor customizado clicando no box e escolhe a opção desejada.

        Args:
            box_locator: Elemento que dispara a abertura da lista de opções.
            option_locator: Opção a ser selecionada após a lista estar visível.
        """
        box = self._resolve_locator(box_locator)
        box.click()
        option = self.wait_for_locator(option_locator)
        option.click()

    def fill(self, locator: Locatable, text: str):
        """Preenche um campo de texto após resolver o locator informado.

        Args:
            locator: Campo de texto a ser preenchido.
            text: Valor a ser inserido no campo.
        """
        self._resolve_locator(locator).fill(text)

    def wait_for_locator(
        self,
        locator: Locatable,
        state: Literal["attached", "detached", "visible", "hidden"] = "visible",
        timeout: Optional[int] = None,
    ) -> Locator:
        """Aguarda um locator atingir o estado desejado e o retorna para encadeamento.

        Args:
            locator: Seletor de string ou locator a ser aguardado.
            state: Estado esperado (visível, oculto, anexado ou removido).
            timeout: Tempo máximo de espera em milissegundos.

        Returns:
            Locator após atingir o estado solicitado.
        """
        resolved = self._resolve_locator(locator)
        resolved.wait_for(state=state, timeout=timeout)
        return resolved

    # ----------------- Validações -----------------------

    def should_see_text(self, text: str, screenshot_on_fail: bool = False, timeout: Optional[int] = None):
        """Valida que um texto visível está presente em tela.

        Em caso de falha, pode capturar evidência caso um serviço de screenshot seja fornecido.

        Args:
            text: Conteúdo textual que deve estar visível.
            screenshot_on_fail: Define se deve registrar evidência em caso de assert falhar.
            timeout: Tempo máximo de espera pela visibilidade do texto.

        Raises:
            AssertionError: Quando o texto não é encontrado dentro do tempo limite.
        """
        logger.info(
            "Validating text visibility",
            extra={"locator_strategy": "get_by_text", "expected_text": text},
        )
        try:
            expect(self.page.get_by_text(text)).to_be_visible(timeout=timeout)
        except AssertionError:
            if screenshot_on_fail and self.screenshot_service:
                self.screenshot_service.save(self.page, f"erro_should_see_{text}")
            raise

    def expect_visible(self, locator: Locatable, timeout: Optional[int] = None):
        """Asserta que o locator está visível dentro do tempo limite informado.

        Args:
            locator: Elemento a ser verificado.
            timeout: Tempo máximo de espera pela visibilidade.
        """
        expect(self._resolve_locator(locator)).to_be_visible(timeout=timeout)

    def expect_hidden(self, locator: Locatable, timeout: Optional[int] = None):
        """Asserta que o locator permanece oculto ou inexistente em tela.

        Args:
            locator: Elemento que deve estar oculto.
            timeout: Tempo máximo de espera pelo estado oculto.
        """
        expect(self._resolve_locator(locator)).to_be_hidden(timeout=timeout)

    def is_visible(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna se o locator está visível sem levantar exceções em falha.

        Args:
            locator: Elemento a ser validado.
            timeout: Tempo máximo de espera pela visibilidade.

        Returns:
            ``True`` quando o elemento está visível dentro do timeout; caso contrário ``False``.
        """
        resolved = self._resolve_locator(locator)
        try:
            return resolved.is_visible(timeout=timeout)
        except Exception:
            return False

    def is_hidden(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Indica se o locator está oculto ou ausente, retornando booleano.

        Args:
            locator: Elemento que deve estar oculto.
            timeout: Tempo máximo de espera pelo estado oculto.

        Returns:
            ``True`` quando o elemento está oculto ou não existe; caso contrário ``False``.
        """
        resolved = self._resolve_locator(locator)
        try:
            return resolved.is_hidden(timeout=timeout)
        except Exception:
            return False

    def expect_text(self, locator: Locatable, text: str, timeout: Optional[int] = None):
        """Verifica se o locator apresenta exatamente o texto esperado.

        Args:
            locator: Elemento que deve apresentar o texto.
            text: Texto completo esperado.
            timeout: Tempo máximo de espera pela validação.
        """
        expect(self._resolve_locator(locator)).to_have_text(text, timeout=timeout)

    def expect_text_contains(self, locator: Locatable, text: str, timeout: Optional[int] = None):
        """Confirma que o locator contém o trecho de texto fornecido.

        Args:
            locator: Elemento que deve conter o texto parcial.
            text: Trecho de texto esperado.
            timeout: Tempo máximo de espera pela validação.
        """
        expect(self._resolve_locator(locator)).to_contain_text(text, timeout=timeout)

    def expect_url_is(self, url: str, timeout: Optional[int] = None):
        """Valida que a URL atual corresponde exatamente ao valor informado.

        Args:
            url: URL completa esperada.
            timeout: Tempo máximo de espera pela coincidência de URL.
        """
        expect(self.page).to_have_url(url, timeout=timeout)

    def expect_url_contains(self, partial_url: str, timeout: Optional[int] = None):
        """Valida que a URL atual contém o fragmento fornecido (escapado como regex).

        Args:
            partial_url: Trecho da URL que deve estar presente.
            timeout: Tempo máximo de espera pela coincidência.
        """
        pattern = re.compile(re.escape(partial_url))
        expect(self.page).to_have_url(pattern, timeout=timeout)

    def expect_title_is(self, title: str, timeout: Optional[int] = None):
        """Confirma que o título da aba coincide exatamente com o texto esperado.

        Args:
            title: Título completo esperado.
            timeout: Tempo máximo de espera pela validação.
        """
        expect(self.page).to_have_title(title, timeout=timeout)

    def expect_title_contains(self, partial_title: str, timeout: Optional[int] = None):
        """Confirma que o título da aba contém o trecho informado (usando regex escapada).

        Args:
            partial_title: Trecho que deve estar presente no título da aba.
            timeout: Tempo máximo de espera pela validação.
        """
        pattern = re.compile(re.escape(partial_title))
        expect(self.page).to_have_title(pattern, timeout=timeout)

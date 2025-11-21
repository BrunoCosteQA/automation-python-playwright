import re
import logging
from typing import Literal, Optional, Union

from playwright.sync_api import Locator, Page, expect
from core.screenshot_service import ScreenshotService

logger = logging.getLogger(__name__)

Locatable = Union[str, Locator]
DEFAULT_TIMEOUT = 30000  # 30s


class BasePage:
    """Camada base para páginas, encapsulando waits, asserts, helpers e serviços auxiliares."""

    # -------------------------------------------------------------------------
    # Construtor / núcleo
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Ações de página (genéricas)
    # -------------------------------------------------------------------------
    def open(self, url: str):
        """Abre uma URL absoluta usando o navegador controlado pelo Playwright."""
        self.page.goto(url)

    def click(
            self,
            locator: Locatable,
            timeout: Optional[int] = None,
            wait_before_ms: int = 0,
    ):
        """
        Realiza um clique no elemento informado, garantindo que ele esteja visível e acionável.

        Este metodo encapsula o comportamento de espera automática do Playwright e permite,
        opcionalmente, adicionar um pequeno delay antes do clique para lidar com componentes
        que necessitam de tempo extra de estabilização (como menus dinâmicos ou elementos
        controlados por JavaScript).

        Args:
            locator (Locatable):
                Seletor CSS/XPath ou instância de ``Locator`` a ser clicada.
                O metodo aceita tanto strings quanto locators já resolvidos.

            timeout (Optional[int]):
                Tempo máximo de espera (em milissegundos) para que o elemento
                atinja o estado de visibilidade antes do clique.
                Caso não seja informado, utiliza o valor padrão ``DEFAULT_TIMEOUT``.

            wait_before_ms (int):
                Tempo (em milissegundos) a aguardar antes de realizar o clique.
                Útil em cenários onde o componente ainda está sendo inicializado ou
                onde o primeiro clique pode disparar comportamentos inesperados caso
                seja executado rápido demais.
                O valor padrão é ``0`` (nenhuma espera adicional).

        Raises:
            TimeoutError:
                Caso o elemento não fique visível dentro do tempo especificado.
        """
        timeout = timeout or DEFAULT_TIMEOUT
        resolved = self._resolve_locator(locator)

        resolved.wait_for(state="visible", timeout=timeout)

        if wait_before_ms:
            self.page.wait_for_timeout(wait_before_ms)

        resolved.click(timeout=timeout)

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

    # -------------------------------------------------------------------------
    # Waits / helpers de locator
    # -------------------------------------------------------------------------
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
        resolved.wait_for(state=state, timeout=timeout or DEFAULT_TIMEOUT)
        return resolved

    def get_visible(self, locator: Locatable, timeout: Optional[int] = None) -> Locator:
        """Resolve o locator e aguarda ele ficar visível antes de retorná-lo.

        Args:
            locator: Seletor de string ou locator a ser aguardado.
            timeout: Tempo máximo de espera em milissegundos.
                     Caso não seja informado, utiliza ``DEFAULT_TIMEOUT``.

        Returns:
            Locator visível, pronto para interação.
        """
        return self.wait_for_locator(
            locator=locator,
            state="visible",
            timeout=timeout or DEFAULT_TIMEOUT,
        )

    def get_hidden(self, locator: Locatable, timeout: Optional[int] = None) -> Locator:
        """Resolve o locator e aguarda ele ficar oculto antes de retorná-lo.

        Args:
            locator: Seletor de string ou locator a ser aguardado.
            timeout: Tempo máximo de espera em milissegundos.
                     Caso não seja informado, utiliza ``DEFAULT_TIMEOUT``.

        Returns:
            Locator após atingir o estado oculto.
        """
        return self.wait_for_locator(
            locator=locator,
            state="hidden",
            timeout=timeout or DEFAULT_TIMEOUT,
        )

    def get_attached(self, locator: Locatable, timeout: Optional[int] = None) -> Locator:
        """Resolve o locator e aguarda ele ser anexado ao DOM (attached).

        Args:
            locator: Seletor de string ou locator a ser aguardado.
            timeout: Tempo máximo de espera em milissegundos.
                     Caso não seja informado, utiliza ``DEFAULT_TIMEOUT``.

        Returns:
            Locator após ser anexado ao DOM.
        """
        return self.wait_for_locator(
            locator=locator,
            state="attached",
            timeout=timeout or DEFAULT_TIMEOUT,
        )

    def get_detached(self, locator: Locatable, timeout: Optional[int] = None) -> Locator:
        """Resolve o locator e aguarda ele ser removido do DOM (detached).

        Args:
            locator: Seletor de string ou locator a ser aguardado.
            timeout: Tempo máximo de espera em milissegundos.
                     Caso não seja informado, utiliza ``DEFAULT_TIMEOUT``.

        Returns:
            Locator após ser removido do DOM.
        """
        return self.wait_for_locator(
            locator=locator,
            state="detached",
            timeout=timeout or DEFAULT_TIMEOUT,
        )

    # -------------------------------------------------------------------------
    # Boolean helpers (para decisão de fluxo)
    # -------------------------------------------------------------------------
    def exists(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna True se o elemento existir no DOM dentro do timeout.

        Não exige visibilidade, apenas presença no DOM.
        """
        timeout = timeout or DEFAULT_TIMEOUT
        resolved = self._resolve_locator(locator)
        try:
            resolved.wait_for(state="attached", timeout=timeout)
            return True
        except Exception:
            return False

    def is_visible(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna True se o elemento estiver visível dentro do timeout."""
        timeout = timeout or DEFAULT_TIMEOUT
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
            True quando o elemento está oculto ou não existe; caso contrário False.
        """
        timeout = timeout or DEFAULT_TIMEOUT
        resolved = self._resolve_locator(locator)
        try:
            return resolved.is_hidden(timeout=timeout)
        except Exception:
            return False

    def is_enabled(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna True se o elemento estiver habilitado (enabled) dentro do timeout."""
        timeout = timeout or DEFAULT_TIMEOUT
        resolved = self._resolve_locator(locator)
        try:
            return resolved.is_enabled(timeout=timeout)
        except Exception:
            return False

    def is_disabled(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna True se o elemento estiver desabilitado (disabled) dentro do timeout."""
        return not self.is_enabled(locator, timeout)

    def is_editable(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna True se o elemento for editável (não readonly + visível)."""
        timeout = timeout or DEFAULT_TIMEOUT
        resolved = self._resolve_locator(locator)
        try:
            return resolved.is_editable(timeout=timeout)
        except Exception:
            return False

    def is_checked(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna True se o elemento estiver marcado (checkbox/radio)."""
        timeout = timeout or DEFAULT_TIMEOUT
        resolved = self._resolve_locator(locator)
        try:
            return resolved.is_checked(timeout=timeout)
        except Exception:
            return False

    def is_clickable(self, locator: Locatable, timeout: Optional[int] = None) -> bool:
        """Retorna True se o elemento estiver visível, habilitado e acionável."""
        timeout = timeout or DEFAULT_TIMEOUT
        resolved = self._resolve_locator(locator)
        try:
            resolved.wait_for(state="visible", timeout=timeout)
            if not resolved.is_enabled(timeout=timeout):
                return False
            # Hover tende a falhar se estiver coberto ou fora de alcance
            resolved.hover(timeout=timeout)
            return True
        except Exception:
            return False

    # -------------------------------------------------------------------------
    # Validações de texto / elementos
    # -------------------------------------------------------------------------
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
            expect(self.page.get_by_text(text)).to_be_visible(timeout=timeout or DEFAULT_TIMEOUT)
        except AssertionError:
            if screenshot_on_fail and self.screenshot_service:
                self.screenshot_service.save(self.page, f"erro_should_see_{text}")
            raise

    def expect_visible(self, locator: Locatable, timeout: Optional[int] = None):
        """Asserta que o locator está visível dentro do tempo limite informado."""
        expect(self._resolve_locator(locator)).to_be_visible(timeout=timeout or DEFAULT_TIMEOUT)

    def expect_hidden(self, locator: Locatable, timeout: Optional[int] = None):
        """Asserta que o locator permanece oculto ou inexistente em tela."""
        expect(self._resolve_locator(locator)).to_be_hidden(timeout=timeout or DEFAULT_TIMEOUT)

    def expect_text(self, locator: Locatable, text: str, timeout: Optional[int] = None):
        """Verifica se o locator apresenta exatamente o texto esperado."""
        expect(self._resolve_locator(locator)).to_have_text(text, timeout=timeout or DEFAULT_TIMEOUT)

    def expect_text_contains(self, locator: Locatable, text: str, timeout: Optional[int] = None):
        """Confirma que o locator contém o trecho de texto fornecido."""
        expect(self._resolve_locator(locator)).to_contain_text(text, timeout=timeout or DEFAULT_TIMEOUT)

    # -------------------------------------------------------------------------
    # Validações de URL / título
    # -------------------------------------------------------------------------
    def expect_url_is(self, url: str, timeout: Optional[int] = None):
        """Valida que a URL atual corresponde exatamente ao valor informado."""
        expect(self.page).to_have_url(url, timeout=timeout or DEFAULT_TIMEOUT)

    def expect_url_contains(self, partial_url: str, timeout: Optional[int] = None):
        """Valida que a URL atual contém o fragmento fornecido (escapado como regex)."""
        pattern = re.compile(re.escape(partial_url))
        expect(self.page).to_have_url(pattern, timeout=timeout or DEFAULT_TIMEOUT)

    def expect_title_is(self, title: str, timeout: Optional[int] = None):
        """Confirma que o título da aba coincide exatamente com o texto esperado."""
        expect(self.page).to_have_title(title, timeout=timeout or DEFAULT_TIMEOUT)

    def expect_title_contains(self, partial_title: str, timeout: Optional[int] = None):
        """Confirma que o título da aba contém o trecho informado (usando regex escapada)."""
        pattern = re.compile(re.escape(partial_title))
        expect(self.page).to_have_title(pattern, timeout=timeout or DEFAULT_TIMEOUT)

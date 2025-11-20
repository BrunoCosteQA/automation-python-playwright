import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class ScreenshotService:
    def __init__(
        self,
        base_dir: str = "evidencias",
        capture_console: bool = True,
        capture_trace: bool = True,
    ):
        self.base_dir = Path(base_dir)
        self.capture_console = capture_console
        self.capture_trace = capture_trace

    def _ensure_dir(self) -> Path:
        date_dir = datetime.now().strftime("%Y-%m-%d")
        dir_path = self.base_dir / date_dir
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def save(self, page, name_prefix: str = "screenshot") -> Optional[Path]:
        """
        Salva screenshot usando Playwright.

        - Respeita DISABLE_SCREENSHOTS=1 (pipeline)
        - Nome único (timestamp + uuid) para paralelismo seguro
        """
        if os.getenv("DISABLE_SCREENSHOTS") == "1":
            return None

        dir_path = self._ensure_dir()
        unique = uuid.uuid4().hex[:8]
        file_name = f"{name_prefix}_{datetime.now().strftime('%H%M%S')}_{unique}.png"
        file_path = dir_path / file_name

        page.screenshot(path=str(file_path), full_page=True)
        return file_path

    def save_console_logs(
        self, messages: List[str], name_prefix: str = "console"
    ) -> Optional[Path]:
        if not self.capture_console or not messages:
            return None

        dir_path = self._ensure_dir()
        unique = uuid.uuid4().hex[:8]
        file_name = f"{name_prefix}_{datetime.now().strftime('%H%M%S')}_{unique}.log"
        file_path = dir_path / file_name

        file_path.write_text("\n".join(messages), encoding="utf-8")
        return file_path

    def export_trace(self, context, name_prefix: str = "trace") -> Optional[Path]:
        if not self.capture_trace:
            return None

        dir_path = self._ensure_dir()
        unique = uuid.uuid4().hex[:8]
        file_name = f"{name_prefix}_{datetime.now().strftime('%H%M%S')}_{unique}.zip"
        file_path = dir_path / file_name

        try:
            context.tracing.stop(path=str(file_path))
        except Exception:
            return None

        return file_path

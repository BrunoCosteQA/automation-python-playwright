import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional


class ScreenshotService:
    def __init__(self, base_dir: str = "evidencias"):
        self.base_dir = Path(base_dir)

    def save(self, page, name_prefix: str = "screenshot") -> Optional[Path]:
        """
        Salva screenshot usando Playwright.

        - Respeita DISABLE_SCREENSHOTS=1 (pipeline)
        - Nome único (timestamp + uuid) para paralelismo seguro
        """
        if os.getenv("DISABLE_SCREENSHOTS") == "1":
            return None

        date_dir = datetime.now().strftime("%Y-%m-%d")
        dir_path = self.base_dir / date_dir
        dir_path.mkdir(parents=True, exist_ok=True)

        unique = uuid.uuid4().hex[:8]
        file_name = f"{name_prefix}_{datetime.now().strftime('%H%M%S')}_{unique}.png"
        file_path = dir_path / file_name

        page.screenshot(path=str(file_path), full_page=True)
        return file_path

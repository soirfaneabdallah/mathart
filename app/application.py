"""QApplication et bootstrap."""

from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from app.window import MainWindow

logger = logging.getLogger(__name__)


def run() -> int:
    """Lance l'application Qt et retourne le code de sortie."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )
    app = QApplication(sys.argv)
    app.setApplicationName("MathArt")
    window = MainWindow()
    window.show()
    logger.info("Application démarrée")
    return app.exec()

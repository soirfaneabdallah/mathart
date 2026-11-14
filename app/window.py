"""Fenêtre principale."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Fenêtre principale de MathArt."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MathArt Vision")
        self.resize(1280, 800)

"""
Minimal GUI adapter for the project.

This module provides a small, resilient `PhishingTool` class so callers can
`from gui import PhishingTool` without importing the larger (and currently
messy) GUI modules. It prefers PyQt5, falls back to PySide6, and raises a
clear RuntimeError only if neither Qt binding is available.

This is intentionally small and dependency-light to avoid importing other
project modules (core/malware) at import time. The full-featured GUI can live
in other modules (e.g. `gui/main_window.py`) and be wired here later.
"""
from __future__ import annotations

"""
Minimal GUI adapter for the project.

This module provides a small, resilient `PhishingTool` class so callers can
`from gui import PhishingTool` without importing the larger (and previously
corrupted) GUI modules. It will try to use the full implementation from
`gui.main_window` when possible, falling back to a minimal placeholder.
"""

try:
    # If the full GUI is available, prefer it
    from .main_window import PhishingTool, USING_QT  # type: ignore
except Exception:
    # Fallback minimal implementation (keeps import-time dependencies small)
    try:
        from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout
        USING_QT = "PyQt5"
    except Exception:
        try:
            from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout
            USING_QT = "PySide6"
        except Exception:
            raise RuntimeError("Install a Qt binding first: `pip install PyQt5` or `pip install PySide6`")

    class PhishingTool(QMainWindow):
        """Minimal placeholder window used when full GUI cannot be imported."""

        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Letsgophishing Pro (minimal)")
            self.setGeometry(100, 100, 800, 600)
            central = QWidget()
            self.setCentralWidget(central)
            layout = QVBoxLayout()
            central.setLayout(layout)
            layout.addWidget(QLabel("PhishingTool (minimal placeholder). Full GUI unavailable."))


__all__ = ["PhishingTool", "USING_QT"]

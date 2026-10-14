"""Composition root: собирает конкретные адаптеры и передаёт их в GUI."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from dataio.adapters import CSVImportSource, JSONProjectRepository, ManualGridSource
from gui.controller import AppController
from gui.main_window import MainWindow


def main() -> int:
    source = ManualGridSource()
    repository = JSONProjectRepository()
    controller = AppController(source=source, repository=repository)

    app = QApplication(sys.argv)
    window = MainWindow(controller=controller)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

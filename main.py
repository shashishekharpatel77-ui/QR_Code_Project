import sys
from PyQt6.QtWidgets import QApplication

from gui import MainWindow
from history_db import init_db


def main():
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
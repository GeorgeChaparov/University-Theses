import sys
from PyQt6.QtWidgets import QApplication

from classes.LabelingApp import LabelingApp

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        w = LabelingApp()
        w.showMaximized()
        w.show()
        sys.exit(app.exec())
    except RuntimeError:
        sys.exit(app.exec())
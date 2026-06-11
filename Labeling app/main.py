import sys
from PyQt6.QtWidgets import QApplication

from classes.LabelingApp import LabelingApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LabelingApp()
    w.showFullScreen()
    w.show()
    sys.exit(app.exec())
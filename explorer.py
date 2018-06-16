#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec_())

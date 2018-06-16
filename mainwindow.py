import webbrowser

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class MainWindow(QMainWindow):
    PROTOCOL_SPEC_URL = 'https://github.com/majorpeter/mprotocol-server/blob/master/README.md'
    ABOUTBOX_MESSAGE = '<b>MProtocol Explorer</b><br/><br/>' \
                       'A simple tool that can be used to walk through the MProtocol property tree.<br/><br/>' \
                       '&copy; 2018 Peter Major'

    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.ui = uic.loadUi('mainwindow.ui', self)

        #TODO self.ui.actionConnect_to.triggered.connect(lambda : print('connect'))
        self.ui.actionOpen_protocol_specification.triggered.connect(lambda : webbrowser.open(MainWindow.PROTOCOL_SPEC_URL))
        self.ui.actionAbout.triggered.connect(lambda : QMessageBox.information(self, 'About', MainWindow.ABOUTBOX_MESSAGE, QMessageBox.Ok))
        self.ui.actionExit.triggered.connect(lambda : self.close())

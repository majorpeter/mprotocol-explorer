import webbrowser

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from mprotocol_client_python.Client import Client
from node_model import NodeModel


class MainWindow(QMainWindow):
    PROTOCOL_SPEC_URL = 'https://github.com/majorpeter/mprotocol-server/blob/master/README.md'
    ABOUTBOX_MESSAGE = '<b>MProtocol Explorer</b><br/><br/>' \
                       'A simple tool that can be used to walk through the MProtocol property tree.<br/><br/>' \
                       '&copy; 2018 Peter Major'

    def __init__(self):
        super(MainWindow, self).__init__(parent=None)

        self.client = None


        self.ui = uic.loadUi('mainwindow.ui', self)

        self.ui.nodeTree.setModel(NodeModel(root_node=self.client.root, parent=self))
        self.ui.nodeTree.selectionModel().currentChanged.connect(self.node_tree_selection_changed)

        #self.ui.actionConnect_to.triggered.connect(lambda : self.connect_to_device()) TODO
        self.ui.actionOpen_protocol_specification.triggered.connect(lambda : webbrowser.open(MainWindow.PROTOCOL_SPEC_URL))
        self.ui.actionAbout.triggered.connect(lambda : QMessageBox.information(self, 'About', MainWindow.ABOUTBOX_MESSAGE, QMessageBox.Ok))
        self.ui.actionExit.triggered.connect(lambda : self.close())

    def connect_to_device(self, ip, port):
        #TODO
        pass

    def node_tree_selection_changed(self, current_index, prev_index):
        print(current_index.internalPointer().get_name())

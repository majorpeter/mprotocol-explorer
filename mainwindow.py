import json
import os
import webbrowser
from html import escape

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QAction

from mprotocol_client_python.Client import Client
from node_model import NodeModel
from properties_panel import PropertiesPanel


class MainWindow(QMainWindow):
    PROTOCOL_SPEC_URL = 'https://github.com/majorpeter/mprotocol-server/blob/master/README.md'
    ABOUTBOX_MESSAGE = '<b>MProtocol Explorer</b><br/><br/>' \
                       'A simple tool that can be used to walk through the MProtocol property tree.<br/><br/>' \
                       '&copy; 2018 Peter Major'
    CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'config.json'

    communication_log_available = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__(parent=None)

        self.load_or_init_config()
        self.client = None
        self.selected_node = None

        self.ui = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'mainwindow.ui', self)
        self.properties_panel = PropertiesPanel(self.ui.propsGroupBox)

        self.ui.actionConnect_to.triggered.connect(self.connect_dialog)
        self.ui.actionOpen_protocol_specification.triggered.connect(lambda : webbrowser.open(MainWindow.PROTOCOL_SPEC_URL))
        self.ui.actionAbout.triggered.connect(lambda : QMessageBox.information(self, 'About', MainWindow.ABOUTBOX_MESSAGE, QMessageBox.Ok))
        self.ui.actionExit.triggered.connect(lambda : self.close())

        self.communication_log_available.connect(self.communication_log_available_slot)

        for entry in self.config['connection_history']:
            self.add_recent_connection_entry(entry)

    def load_or_init_config(self):
        try:
            with open(MainWindow.CONFIG_PATH, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {'connection_history': []}

    def save_config(self):
        with open(MainWindow.CONFIG_PATH, 'w') as f:
            json.dump(self.config, f)

    def connect_dialog(self):
        entry_text, ok = QInputDialog.getText(self, 'Connect to device...', 'Enter IP address and port (<ip>:<port>)')
        if ok:
            entry_sections = entry_text.split(':')
            try:
                ip = entry_sections[0]
                port = int(entry_sections[1])
            except IndexError:
                QMessageBox.warning(self, 'Error', 'Invalid address!')
                return

            self.connect_to_device(ip, port)
            if entry_text not in self.config['connection_history']:
                self.config['connection_history'].append(entry_text)
                self.save_config()
                self.add_recent_connection_entry(entry_text)

    def add_recent_connection_entry(self, entry):
        self.ui.menuRecent_Connections.setEnabled(True)
        action = QAction(entry, self)
        action.triggered.connect(lambda : self.connect_to_device(entry.split(':')[0], int(entry.split(':')[1])))
        self.ui.menuRecent_Connections.addAction(action)

    def connect_to_device(self, ip, port):
        self.client = Client(ip, port, timeout=1)
        self.client.set_trace_callbacks(self.communication_log_rx, self.communication_log_tx)

        self.ui.nodeTree.setModel(NodeModel(root_node=self.client.root, parent=self))
        self.ui.nodeTree.selectionModel().currentChanged.connect(self.node_tree_selection_changed)

    def communication_log_rx(self, message):
        self.communication_log_available.emit('<span style="color: #D9D9D9">◀</span> <span style="color: #FF5D26">%s</span>' % escape(message))

    def communication_log_tx(self, message):
        self.communication_log_available.emit('<span style="color: #D9D9D9">▶</span> <span style="color: #2CB1DE">%s</span>' % escape(message))

    def communication_log_available_slot(self, html):
        self.ui.commLogView.append(html)
        self.truncate_communication_log()

    def truncate_communication_log(self):
        while self.ui.commLogView.document().blockCount() > 10:
            cursor = self.ui.commLogView.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()
        self.ui.commLogView.moveCursor(QTextCursor.End)

    def node_tree_selection_changed(self, current_index, prev_index):
        self.update_props_panel(current_index.internalPointer())

    def update_props_panel(self, node):
        self.selected_node = node
        self.ui.propsGroupBox.setTitle(node.get_name())
        self.properties_panel.display_node(node)

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton


class PropertiesPanel(QObject):
    def __init__(self, parent):
        super(PropertiesPanel, self).__init__(parent)
        self.grid = QGridLayout(parent)

    def display_node(self, node):
        self.clear_layout()

        manual_label = QLabel(node.get_node_manual())
        self.grid.addWidget(manual_label, 0, 0)

        props = node.get_properties()
        for i in range(len(props)):
            self.grid.addWidget(QLabel(props[i].data['name']), i + 1, 0)

    def clear_layout(self):
        while not self.grid.isEmpty():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

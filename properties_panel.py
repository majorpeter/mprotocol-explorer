from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy


class PropertiesPanel(QObject):
    COLS_COUNT = 3

    def __init__(self, parent):
        super(PropertiesPanel, self).__init__(parent)
        self.grid = QGridLayout(parent)

    def display_node(self, node):
        self.clear_layout()

        manual_label = QLabel(node.get_node_manual())
        self.grid.addWidget(manual_label, 0, 0, 1, PropertiesPanel.COLS_COUNT)

        props = node.get_properties()
        property_index = 0
        for prop in props:
            name_label = QLabel(prop.data['name'])
            self.grid.addWidget(name_label, property_index + 1, 0)
            property_index += 1

        vertical_fill = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.grid.addItem(vertical_fill, property_index + 2, 0, 1, PropertiesPanel.COLS_COUNT)

    def clear_layout(self):
        while not self.grid.isEmpty():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

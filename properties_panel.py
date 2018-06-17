from enum import Enum

from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QLineEdit, QMessageBox


class PropertiesPanel(QObject):
    COLS_COUNT = 5
    PROPERTY_PROPNAME = 'propName'
    PROPERTY_EDITOR = 'editor'

    class EditDecoration(Enum):
        Default = 0
        Success = 1
        Error = 2
        Blink = 3

    def __init__(self, parent):
        super(PropertiesPanel, self).__init__(parent)
        self.grid = QGridLayout(parent)
        self.node = None

    def display_node(self, node):
        self.clear_layout()
        self.node = node

        manual_label = QLabel(node.get_node_manual())
        self.grid.addWidget(manual_label, 0, 0, 1, PropertiesPanel.COLS_COUNT)

        props = node.get_properties()
        property_index = 0
        for prop in props:
            type_label = QLabel(prop.data['type'])
            type_label.setStyleSheet('font-size: 8pt; font-style: italic;')
            self.grid.addWidget(type_label, property_index + 1, 0)

            name_label = QLabel(prop.data['name'])
            self.grid.addWidget(name_label, property_index + 1, 1)

            editor = QLineEdit()
            editor.setText(prop.data['value'])
            editor.setProperty(PropertiesPanel.PROPERTY_PROPNAME, prop.data['name'])
            self.grid.addWidget(editor, property_index + 1, 2)

            if prop.data['writable']:
                set_button = QPushButton()
                set_button.setText('Set')
                set_button.setProperty(PropertiesPanel.PROPERTY_PROPNAME, prop.data['name'])
                set_button.setProperty(PropertiesPanel.PROPERTY_EDITOR, editor)
                set_button.clicked.connect(self.on_set_button_pushed)
                self.grid.addWidget(set_button, property_index + 1, 3)
            if prop.data['type'] == 'METHOD':
                call_button = QPushButton()
                call_button.setText('Call')
                call_button.setProperty(PropertiesPanel.PROPERTY_PROPNAME, prop.data['name'])
                call_button.setProperty(PropertiesPanel.PROPERTY_EDITOR, editor)
                call_button.clicked.connect(self.on_call_button_pushed)
                self.grid.addWidget(call_button, property_index + 1, 3)

            man_button = QPushButton()
            man_button.setText('Manual')
            man_button.setProperty(PropertiesPanel.PROPERTY_PROPNAME, prop.data['name'])
            man_button.clicked.connect(self.on_manual_button_pushed)
            self.grid.addWidget(man_button, property_index + 1, 4)
            property_index += 1

        vertical_fill = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.grid.addItem(vertical_fill, property_index + 2, 0, 1, PropertiesPanel.COLS_COUNT)

    def on_set_button_pushed(self):
        property_name = self.sender().property(PropertiesPanel.PROPERTY_PROPNAME)
        property_editor = self.sender().property(PropertiesPanel.PROPERTY_EDITOR)
        property_value = property_editor.text()
        try:
            self.node[property_name] = property_value
            self.decorate_editor(property_editor, PropertiesPanel.EditDecoration.Success)
        except BaseException as e:
            self.decorate_editor(property_editor, PropertiesPanel.EditDecoration.Error)
            print(e)

    def on_call_button_pushed(self):
        property_name = self.sender().property(PropertiesPanel.PROPERTY_PROPNAME)
        property_editor = self.sender().property(PropertiesPanel.PROPERTY_EDITOR)
        property_value = property_editor.text()
        result = self.node.__getattr__(property_name)(property_value)
        if result:
            self.decorate_editor(property_editor, PropertiesPanel.EditDecoration.Success)
        else:
            self.decorate_editor(property_editor, PropertiesPanel.EditDecoration.Error)

    def on_manual_button_pushed(self):
        property_name = self.sender().property(PropertiesPanel.PROPERTY_PROPNAME)
        manual_string = self.node.__getattr__(property_name).get_property_manual()
        QMessageBox.information(self.parent(), 'Manual', manual_string)

    def decorate_editor(self, editor, decoration, timeout_sec=1):
        if decoration == PropertiesPanel.EditDecoration.Default:
            editor.setStyleSheet('')
        elif decoration == PropertiesPanel.EditDecoration.Success:
            editor.setStyleSheet('background: #ccffcc;')
        elif decoration == PropertiesPanel.EditDecoration.Error:
            editor.setStyleSheet('background: #ffcccc;')
        elif decoration == PropertiesPanel.EditDecoration.Blink:
            editor.setStyleSheet('background: #ffffee; color: #0000de')

        # clear decoration after timeout
        if timeout_sec != 0:
            QTimer.singleShot(timeout_sec * 1000,
                      lambda : self.decorate_editor(editor, PropertiesPanel.EditDecoration.Default, timeout_sec=0))

    def clear_layout(self):
        while not self.grid.isEmpty():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

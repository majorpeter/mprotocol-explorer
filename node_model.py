from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt


class NodeModel(QAbstractItemModel):
    def __init__(self, root_node, parent=None):
        super(NodeModel, self).__init__(parent=parent)
        self.root_node = root_node

    def headerData(self, section, orientation, role):
        return QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.root_node
        else:
            parentItem = parent.internalPointer()

        children = parentItem.get_children()
        if row < len(children):
            return self.createIndex(row, column, children[row])
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item._parent

        if parent_item == self.root_node:
            return QModelIndex()

        #grandparent_item = parent_item._parent
        return self.createIndex(0, 0, parent_item) #TODO row

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.root_node
        else:
            parentItem = parent.internalPointer()

        return len(parentItem.get_children())

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return index.internalPointer().get_name()

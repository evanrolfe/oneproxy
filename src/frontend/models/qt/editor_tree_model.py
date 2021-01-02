from PySide2 import QtCore, QtGui
from PySide2.QtCore import QAbstractItemModel, Qt
from PySide2.QtGui import QIcon

from models.qt.editor_tree_item import EditorTreeItem

class EditorTreeModel(QAbstractItemModel):
  def __init__(self, header, editor_items, parent=None):
    super(EditorTreeModel, self).__init__(parent)

    self.rootItem = EditorTreeItem(header)
    self.setup_model_data(editor_items, self.rootItem)

  def supportedDropActions(self):
    return Qt.MoveAction | Qt.CopyAction

  def columnCount(self, parent=QtCore.QModelIndex()):
    return self.rootItem.columnCount()

  def data(self, index, role):
    if not index.isValid():
      return None

    if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole and role != QtCore.Qt.DecorationRole:
      return None

    item = self.getItem(index)

    if role == QtCore.Qt.DecorationRole:
      return item.icon()
    else:
      return item.data(index.column())

  def flags(self, index):
    if not index.isValid():
      return None

    return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

  def getItem(self, index):
    if index.isValid():
      item = index.internalPointer()
      if item:
        return item

    return self.rootItem

  def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
    if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
      return self.rootItem.data(section)

    return None

  def index(self, row, column, parent=QtCore.QModelIndex()):
    if parent.isValid() and parent.column() != 0:
      return QtCore.QModelIndex()

    parentItem = self.getItem(parent)
    childItem = parentItem.child(row)
    if childItem:
      return self.createIndex(row, column, childItem)
    else:
      return QtCore.QModelIndex()

  def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
    parentItem = self.getItem(parent)
    self.beginInsertRows(parent, position, position + rows - 1)
    success = parentItem.insertChildren(position, rows, self.rootItem.columnCount())
    self.endInsertRows()

    return success

  def parent(self, index):
    if not index.isValid():
      return QtCore.QModelIndex()

    childItem = self.getItem(index)
    parentItem = childItem.parent

    if parentItem == self.rootItem:
      return QtCore.QModelIndex()

    return self.createIndex(parentItem.childNumber(), 0, parentItem)

  def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
    parentItem = self.getItem(parent)

    self.beginRemoveRows(parent, position, position + rows - 1)
    success = parentItem.removeChildren(position, rows)
    self.endRemoveRows()

    return success

  def rowCount(self, parent=QtCore.QModelIndex()):
    parentItem = self.getItem(parent)

    return parentItem.childCount()

  def hasChildren(self, index):
    item = self.getItem(index)

    if (item == None):
      return False

    if item.is_dir:
      return True

    return (item.childCount() > 0)

  def setup_model_data(self, editor_items, root_tree_item):
    root_level_editor_items = [x for x in editor_items if x.parent_id == None]

    for editor_item in root_level_editor_items:
      self.add_editor_item_to_tree(root_tree_item, editor_item)

  def add_editor_item_to_tree(self, parent_tree_item, editor_item):
    tree_item = EditorTreeItem.from_editor_item(editor_item)

    parent_tree_item.insertChild(tree_item)

    for child_editor_item in editor_item.children():
      self.add_editor_item_to_tree(tree_item, child_editor_item)

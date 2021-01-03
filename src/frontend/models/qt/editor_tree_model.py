from PySide2 import QtCore, QtGui
from PySide2.QtCore import QAbstractItemModel, Qt, QDataStream, QByteArray
from PySide2.QtGui import QIcon
import json

from models.qt.editor_tree_item import EditorTreeItem

class EditorTreeModel(QAbstractItemModel):
  def __init__(self, header, editor_items, parent=None):
    super(EditorTreeModel, self).__init__(parent)

    self.rootItem = EditorTreeItem(header, None, True)
    self.setup_model_data(editor_items, self.rootItem)

  def supportedDropActions(self):
    return Qt.MoveAction | Qt.CopyAction

  def columnCount(self, parent=QtCore.QModelIndex()):
    return self.rootItem.columnCount()

  def data(self, index, role):
    if not index.isValid():
      return None

    if role != Qt.DisplayRole and role != Qt.EditRole and role != Qt.DecorationRole:
      return None

    item = self.getItem(index)

    if role == Qt.DecorationRole:
      return item.icon()
    else:
      return item.data()

  def setData(self, index, value, role=Qt.EditRole):
    if role == Qt.EditRole:
      item = self.getItem(index)
      item.setLabel(value)

      self.dataChanged.emit(index, index, role)
      return True

    elif role == Qt.DisplayRole:
      self.dataChanged.emit(index, index, role)
      return True

    return False

  def mimeTypes(self):
    return ['text/index-json-array']

  def mimeData(self, indexes):
    tree_items = [self.getItem(i) for i in indexes]
    index_data = [{ 'internalId': i.internalId(), 'row': i.row(), 'column': i.column() } for i in indexes]

    encoded_json = json.dumps(index_data).encode()
    mimeData = QtCore.QMimeData()
    mimeData.setData('text/index-json-array', QByteArray(encoded_json))
    return mimeData

  def canDropMimeData(self, data, action, row, column, parent_index):
    if (action != Qt.DropAction.MoveAction):
      return False

    item = self.getItem(parent_index)
    return (item.is_dir == True)

  def dropMimeData(self, data, action, row, column, parent_index):
    if (action != Qt.DropAction.MoveAction):
      return False

    if not parent_index.isValid():
      print('DROPPED ON ROOT!!!!!!!!!!!!!')

    encoded_data = data.data('text/index-json-array')
    index_data = json.loads(str(encoded_data, 'utf-8'))

    indexes = [self.createIndex(i['row'], i['column'], i['internalId']) for i in index_data]
    tree_items = [self.getItem(i) for i in indexes]

    rows = sorted([i.row() for i in indexes])
    diff = rows[-1] - rows[0]
    self.removeRows(rows[0], diff+1, indexes[0].parent())

    self.insertChildren(tree_items, parent_index)

    return True

  def flags(self, index):
    if not index.isValid():
      return Qt.NoItemFlags| Qt.ItemIsDropEnabled

    return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

  def getItem(self, index):
    if index.isValid():
      item = index.internalPointer()
      if item:
        return item

    return self.rootItem

  def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
    if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
      return self.rootItem.data()

    return None

  def index(self, row, column, parent_index=QtCore.QModelIndex()):
    if parent_index.isValid() and parent_index.column() != 0:
      return QtCore.QModelIndex()

    parentItem = self.getItem(parent_index)
    childItem = parentItem.child(row)

    if childItem:
      return self.createIndex(row, column, childItem)
    else:
      return QtCore.QModelIndex()

  # TODO: Make this call self.insertChildren()
  def insertChild(self, child, parent=QtCore.QModelIndex()):
    parentItem = self.getItem(parent)
    position = parentItem.childCount()

    self.beginInsertRows(parent, position, position)
    success = parentItem.insertChild(child)
    self.endInsertRows()

    return success

  def insertChildren(self, child_items, parent_index=QtCore.QModelIndex()):
    parentItem = self.getItem(parent_index)
    position = parentItem.childCount()

    self.beginInsertRows(parent_index, position, position + len(child_items))
    success = parentItem.insertChildren(child_items)
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

  def removeRows(self, position, rows, parent_index=QtCore.QModelIndex()):
    parentItem = self.getItem(parent_index)

    self.beginRemoveRows(parent_index, position, position + rows)
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

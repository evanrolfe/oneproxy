from PySide2 import QtCore, QtGui
from PySide2.QtCore import QAbstractItemModel, Qt
from PySide2.QtGui import QIcon

from models.qt.editor_tree_item import EditorTreeItem

class EditorTreeModel(QAbstractItemModel):
  def __init__(self, headers, data, parent=None):
    super(EditorTreeModel, self).__init__(parent)

    rootData = [header for header in headers]
    self.rootItem = EditorTreeItem(rootData)
    self.setupModelData(data.split("\n"), self.rootItem)

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

  def setupModelData(self, lines, parent):
    # Level 0
    admin_area = EditorTreeItem('Admin Area', None, True)
    parent.insertChild(admin_area)

    user_area = EditorTreeItem('User Area', None, True)
    parent.insertChild(user_area)

    public_area = EditorTreeItem('Public Area', None, True)
    parent.insertChild(public_area)

    # Level 1
    xss = EditorTreeItem('XSS', None, True)
    admin_area.insertChild(xss)

    sqli = EditorTreeItem('SQLi', None, True)
    admin_area.insertChild(sqli)

    biz_logic = EditorTreeItem('Business Logic Exploits', None, True)
    user_area.insertChild(biz_logic)

    account = EditorTreeItem('GET /account.json', None, False)
    user_area.insertChild(account)

    # Level 2
    post1 = EditorTreeItem('GET /api/posts.json', None, False)
    xss.insertChild(post1)

    post2 = EditorTreeItem('POST /api/posts.json', None, False)
    xss.insertChild(post2)

    posts3 = EditorTreeItem('POST /api/posts.json', None, False)
    sqli.insertChild(posts3)

    account2 = EditorTreeItem('GET /account.json', None, False)
    biz_logic.insertChild(account2)

    return True

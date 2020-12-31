from PySide2 import QtCore, QtGui
from PySide2.QtCore import QAbstractItemModel, Qt
from PySide2.QtGui import QIcon

from models.qt.request_groups_tree_item import RequestGroupsTreeItem

class RequestGroupsTreeModel(QAbstractItemModel):
  def __init__(self, headers, data, parent=None):
    super(RequestGroupsTreeModel, self).__init__(parent)

    rootData = [header for header in headers]
    self.rootItem = RequestGroupsTreeItem(rootData)
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

  def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
    self.beginInsertColumns(parent, position, position + columns - 1)
    success = self.rootItem.insertColumns(position, columns)
    self.endInsertColumns()

    return success

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
    parentItem = childItem.parent()

    if parentItem == self.rootItem:
      return QtCore.QModelIndex()

    return self.createIndex(parentItem.childNumber(), 0, parentItem)

  def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
    self.beginRemoveColumns(parent, position, position + columns - 1)
    success = self.rootItem.removeColumns(position, columns)
    self.endRemoveColumns()

    if self.rootItem.columnCount() == 0:
      self.removeRows(0, rowCount())

    return success

  def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
    parentItem = self.getItem(parent)

    self.beginRemoveRows(parent, position, position + rows - 1)
    success = parentItem.removeChildren(position, rows)
    self.endRemoveRows()

    return success

  def rowCount(self, parent=QtCore.QModelIndex()):
    parentItem = self.getItem(parent)

    return parentItem.childCount()

  def setData(self, index, value, role=QtCore.Qt.EditRole):
    if role != QtCore.Qt.EditRole:
      return False

    item = self.getItem(index)
    result = item.setData(index.column(), value)

    if result:
      self.dataChanged.emit(index, index)

    return result

  def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
    if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
      return False

    result = self.rootItem.setData(section, value)
    if result:
      self.headerDataChanged.emit(orientation, section, section)

    return result

  def setupModelData(self, lines, parent):
    parents = [parent]
    indentations = [0]

    number = 0

    while number < len(lines):
      position = 0
      while position < len(lines[number]):
        if lines[number][position] != " ":
          break
        position += 1

      lineData = lines[number][position:].strip()

      if lineData:
        # Read the column data from the rest of the line.
        columnData = [s for s in lineData.split('\t') if s]

        if position > indentations[-1]:
          # The last child of the current parent is now the new
          # parent unless the current parent has no children.

          if parents[-1].childCount() > 0:
            parents.append(parents[-1].child(parents[-1].childCount() - 1))
            indentations.append(position)

        else:
          while position < indentations[-1] and len(parents) > 0:
            parents.pop()
            indentations.pop()

        # Append a new item to the current parent's list of children.
        parent = parents[-1]
        parent.insertChildren(parent.childCount(), 1, self.rootItem.columnCount())
        for column in range(len(columnData)):
          parent.child(parent.childCount() -1).setData(column, columnData[column])

      number += 1

from PySide2.QtGui import QIcon

class RequestGroupsTreeItem():
  def __init__(self, data, parent=None):
    self.parentItem = parent
    self.itemData = data
    self.childItems = []

  def child(self, row):
    return self.childItems[row]

  def childCount(self):
    return len(self.childItems)

  def childNumber(self):
    if self.parentItem != None:
      return self.parentItem.childItems.index(self)
    return 0

  def columnCount(self):
    return len(self.itemData)

  def icon(self):
    if (len(self.childItems) == 0):
      return QIcon(":/icons/dark/icons8-plus-math-50.png")
    else:
      return None

  def data(self, column):
    return self.itemData[column]

  def insertChildren(self, position, count, columns):
    if position < 0 or position > len(self.childItems):
      return False

    for row in range(count):
      data = [None for v in range(columns)]
      item = RequestGroupsTreeItem(data, self)
      self.childItems.insert(position, item)

    return True

  def insertColumns(self, position, columns):
    if position < 0 or position > len(self.itemData):
      return False

    for column in range(columns):
      self.itemData.insert(position, None)

    for child in self.childItems:
      child.insertColumns(position, columns)

    return True

  def parent(self):
    return self.parentItem

  def removeChildren(self, position, count):
    if position < 0 or position + count > len(self.childItems):
      return False

    for row in range(count):
      self.childItems.pop(position)

    return True

  def removeColumns(self, position, columns):
    if position < 0 or position + columns > len(self.itemData):
      return False

    for column in range(columns):
      self.itemData.pop(position)

    for child in self.childItems:
      child.removeColumns(position, columns)

    return True

  def setData(self, column, value):
    if column < 0 or column >= len(self.itemData):
      return False

    self.itemData[column] = value

    return True


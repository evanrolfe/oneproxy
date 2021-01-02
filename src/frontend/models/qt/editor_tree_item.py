from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QTreeWidgetItem

class EditorTreeItem():
  def __init__(self, label, editor_item = None, is_dir = False, parent=None):
    self.parent = parent
    self.label = label
    self.is_dir = is_dir
    self.editor_item = editor_item
    self.childItems = []

  #-----------------------------------------------------------------------------
  # QT API Methods:
  #-----------------------------------------------------------------------------
  def data(self, column):
    return self.label

  def child(self, row):
    return self.childItems[row]

  def childCount(self):
    return len(self.childItems)

  def childNumber(self):
    if self.parent != None:
      return self.parent.childItems.index(self)
    return 0

  def childIndicatorPolicy(self):
    return QTreeWidgetItem.ShowIndicator

  def columnCount(self):
    return 1

  def insertChild(self, child_item):
    self.childItems.append(child_item)
    child_item.parent = self

  def removeChildren(self, position, count):
    if position < 0 or position + count > len(self.childItems):
      return False

    for row in range(count):
      self.childItems.pop(position)

    return True

  #-----------------------------------------------------------------------------
  # "Custom" Methods:
  #-----------------------------------------------------------------------------
  def icon(self):
    if self.is_dir:
      return None
    else:
      return QIcon(":/icons/dark/icons8-plus-math-50.png")


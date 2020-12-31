import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView, QTabBar
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon

from ui_compiled.requests.ui_requests_page import Ui_RequestsPage

from models.request_groups_tree_model import RequestGroupsTreeModel
from lib.backend import Backend

DATA = """
Admin Area
    Launching Designer
    The User Interface

User Area
    Creating a Dialog
    Composing the Dialog
    Creating a Layout
    Signal and Slot Connections

Checkout Process
    The Direct Approach
    The Single Inheritance Approach
    The Multiple Inheritance Approach
    Automatic Connections
        A Dialog Without Auto-Connect
        A Dialog With Auto-Connect
"""

class RequestsPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(RequestsPage, self).__init__(*args, **kwargs)

    self.ui = Ui_RequestsPage()
    self.ui.setupUi(self)

    headers = ["Requests"]
    tree_model = RequestGroupsTreeModel(headers, DATA)
    self.ui.requestGroupsTreeView.setModel(tree_model)

    self.ui.requestGroupsTreeView.setDragDropMode(QAbstractItemView.InternalMove)
    self.ui.requestGroupsTreeView.setSelectionMode(QAbstractItemView.SingleSelection)
    self.ui.requestGroupsTreeView.setDragEnabled(True)
    self.ui.requestGroupsTreeView.setAcceptDrops(True)

    self.ui.openRequestTabs.setTabsClosable(True)
    self.ui.openRequestTabs.setMovable(True)

    tab_bar = self.ui.openRequestTabs.tabBar()
   # tab_bar.tabButton(0, QTabBar.RightSide).deleteLater()
    #tab_bar.setTabButton(2, QTabBar.RightSide, QIcon(":/icons/dark/icons8-plus-math-50.png"))
    #tab_bar.setTabIcon(2, )

    #self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)

    #self.ui.requestGroupsTreeView.selectionModel().selectionChanged.connect(self.updateActions)

    #self.ui.actionsMenu.aboutToShow.connect(self.updateActions)
    # self.insertRowAction.triggered.connect(self.insertRow)
    # self.insertColumnAction.triggered.connect(self.insertColumn)
    # self.removeRowAction.triggered.connect(self.removeRow)
    # self.removeColumnAction.triggered.connect(self.removeColumn)
    # self.insertChildAction.triggered.connect(self.insertChild)

    # self.updateActions()

  def insertChild(self):
      index = self.ui.requestGroupsTreeView.selectionModel().currentIndex()
      model = self.ui.requestGroupsTreeView.model()

      if model.columnCount(index) == 0:
          if not model.insertColumn(0, index):
              return

      if not model.insertRow(0, index):
          return

      for column in range(model.columnCount(index)):
          child = model.index(0, column, index)
          model.setData(child, "[No data]",
                  QtCore.Qt.EditRole)
          if not model.headerData(column, QtCore.Qt.Horizontal).isValid():
              model.setHeaderData(column, QtCore.Qt.Horizontal,
                      "[No header]", QtCore.Qt.EditRole)

      self.ui.requestGroupsTreeView.selectionModel().setCurrentIndex(model.index(0, 0, index),
              QtGui.QItemSelectionModel.ClearAndSelect)
      self.updateActions()

  def insertColumn(self, parent=QtCore.QModelIndex()):
      model = self.ui.requestGroupsTreeView.model()
      column = self.ui.requestGroupsTreeView.selectionModel().currentIndex().column()

      # Insert a column in the parent item.
      changed = model.insertColumn(column + 1, parent)
      if changed:
          model.setHeaderData(column + 1, QtCore.Qt.Horizontal,
                  "[No header]", QtCore.Qt.EditRole)

      self.updateActions()

      return changed

  def insertRow(self):
      index = self.ui.requestGroupsTreeView.selectionModel().currentIndex()
      model = self.ui.requestGroupsTreeView.model()

      if not model.insertRow(index.row()+1, index.parent()):
          return

      self.updateActions()

      for column in range(model.columnCount(index.parent())):
          child = model.index(index.row()+1, column, index.parent())
          model.setData(child, "[No data]", QtCore.Qt.EditRole)

  def removeColumn(self, parent=QtCore.QModelIndex()):
      model = self.ui.requestGroupsTreeView.model()
      column = self.ui.requestGroupsTreeView.selectionModel().currentIndex().column()

      # Insert columns in each child of the parent item.
      changed = model.removeColumn(column, parent)

      if not parent.isValid() and changed:
          self.updateActions()

      return changed

  def removeRow(self):
      index = self.ui.requestGroupsTreeView.selectionModel().currentIndex()
      model = self.ui.requestGroupsTreeView.model()

      if (model.removeRow(index.row(), index.parent())):
          self.updateActions()

  def updateActions(self):
      hasSelection = not self.ui.requestGroupsTreeView.selectionModel().selection().isEmpty()
      self.ui.removeRowAction.setEnabled(hasSelection)
      self.ui.removeColumnAction.setEnabled(hasSelection)

      hasCurrent = self.ui.requestGroupsTreeView.selectionModel().currentIndex().isValid()
      self.ui.insertRowAction.setEnabled(hasCurrent)
      self.ui.insertColumnAction.setEnabled(hasCurrent)

      if hasCurrent:
          self.ui.requestGroupsTreeView.closePersistentEditor(self.ui.requestGroupsTreeView.selectionModel().currentIndex())

          row = self.ui.requestGroupsTreeView.selectionModel().currentIndex().row()
          column = self.ui.requestGroupsTreeView.selectionModel().currentIndex().column()
          if self.ui.requestGroupsTreeView.selectionModel().currentIndex().parent().isValid():
              self.statusBar().showMessage("Position: (%d,%d)" % (row, column))
          else:
              self.statusBar().showMessage("Position: (%d,%d) in top level" % (row, column))

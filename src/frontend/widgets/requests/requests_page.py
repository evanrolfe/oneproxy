import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView, QTabBar, QMenu, QAction, QItemDelegate, QMessageBox
from PySide2.QtCore import QFile, Slot, Qt, QItemSelectionModel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon

from views._compiled.requests.ui_requests_page import Ui_RequestsPage

from lib.app_settings import AppSettings
from models.data.editor_item import EditorItem
from models.qt.editor_tree_model import EditorTreeModel
from models.qt.editor_tree_item import EditorTreeItem
from lib.backend import Backend

class RequestsPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(RequestsPage, self).__init__(*args, **kwargs)

    self.ui = Ui_RequestsPage()
    self.ui.setupUi(self)

    editor_items = EditorItem.all()
    self.tree_model = EditorTreeModel('Requests', editor_items)
    self.ui.requestGroupsTreeView.setModel(self.tree_model)

    self.ui.requestGroupsTreeView.setDragDropMode(QAbstractItemView.InternalMove)
    self.ui.requestGroupsTreeView.setSelectionMode(QAbstractItemView.SingleSelection)
    self.ui.requestGroupsTreeView.setDragEnabled(True)
    self.ui.requestGroupsTreeView.setAcceptDrops(True)
    self.ui.requestGroupsTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.ui.requestGroupsTreeView.customContextMenuRequested.connect(self.open_menu)

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
    self.restore_layout_state()

  # TODO DRY up this method and save_layout_state()
  def restore_layout_state(self):
    settings = AppSettings.get_instance()
    splitter_state = settings.get("RequestsPage.splitter", None)
    self.ui.splitter.restoreState(splitter_state)

  def save_layout_state(self):
    splitter_state = self.ui.splitter.saveState()
    settings = AppSettings.get_instance()
    settings.save("RequestsPage.splitter", splitter_state)

    self.ui.requestGroupView.save_layout_state()

  @Slot()
  def open_menu(self, position):
    index = self.ui.requestGroupsTreeView.indexAt(position)

    if not index.isValid():
      print(index)
      return

    new_request_action = QAction("New Request")
    new_request_action.triggered.connect(lambda: self.new_request_clicked(index))

    new_dir_action = QAction("New Folder")
    new_dir_action.triggered.connect(lambda: self.new_dir_clicked(index))

    rename_action = QAction("Rename")
    rename_action.triggered.connect(lambda: self.ui.requestGroupsTreeView.edit(index))

    delete_action = QAction("Delete")
    delete_action.triggered.connect(lambda: self.delete_clicked(index))

    menu = QMenu(self)
    menu.addAction(new_request_action)
    menu.addAction(new_dir_action)
    menu.addAction(rename_action)
    menu.addAction(delete_action)
    menu.exec_(self.ui.requestGroupsTreeView.viewport().mapToGlobal(position))

  @Slot()
  def new_request_clicked(self, parent_index):
    child_editor_item = EditorItem()
    child_editor_item.name = 'new request'
    child_editor_item.item_type = 'request'

    self.insertChild(child_editor_item, parent_index)

  @Slot()
  def new_dir_clicked(self, parent_index):
    child_editor_item = EditorItem()
    child_editor_item.name = 'new folder'
    child_editor_item.item_type = 'dir'

    self.insertChild(child_editor_item, parent_index)

  @Slot()
  def delete_clicked(self, index):
    print(f"Deleting! {index}")

    tree_item = self.tree_model.getItem(index)

    if tree_item.is_dir:
      message = 'Are you sure you want to delete this folder and all of its children?'
    else:
      message = 'Are you sure you want to delete this request?'

    message_box = QMessageBox()
    message_box.setWindowTitle('PNTest')
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    message_box.setDefaultButton(QMessageBox.Yes)
    response = message_box.exec_()

    if response == QMessageBox.Yes:
      self.tree_model.removeRows(index.row(), 1, index.parent())

  def insertChild(self, child_editor_item, parent_index):
    parent_tree_item = self.tree_model.getItem(parent_index)

    child_editor_item.parent_id = parent_tree_item.editor_item.id
    child_editor_item.save()

    child_tree_item = EditorTreeItem.from_editor_item(child_editor_item)

    self.tree_model.insertChild(child_tree_item, parent_index)

    child_index = self.tree_model.index(parent_tree_item.childCount()-1, 0, parent_index)

    self.ui.requestGroupsTreeView.selectionModel().setCurrentIndex(
      child_index,
      QItemSelectionModel.ClearAndSelect
    )

    self.ui.requestGroupsTreeView.edit(child_index)

  def removeRow(self):
      index = self.ui.requestGroupsTreeView.selectionModel().currentIndex()
      model = self.ui.requestGroupsTreeView.model()

      if (model.removeRow(index.row(), index.parent())):
          self.updateActions()


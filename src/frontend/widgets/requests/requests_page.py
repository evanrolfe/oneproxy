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

    editor_items = EditorItem.order_by('item_type', 'asc').get()
    self.tree_model = EditorTreeModel('Requests', editor_items)
    self.tree_model.change_selection.connect(self.change_selection)

    self.ui.requestGroupsTreeView.setModel(self.tree_model)
    self.ui.requestGroupsTreeView.setDragDropMode(QAbstractItemView.InternalMove)
    self.ui.requestGroupsTreeView.setSelectionMode(QAbstractItemView.ContiguousSelection)
    self.ui.requestGroupsTreeView.setDragEnabled(True)
    self.ui.requestGroupsTreeView.setAcceptDrops(True)
    self.ui.requestGroupsTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.ui.requestGroupsTreeView.customContextMenuRequested.connect(self.right_click)
    self.ui.requestGroupsTreeView.setDragDropOverwriteMode(True)

    self.ui.openRequestTabs.setTabsClosable(True)
    self.ui.openRequestTabs.setMovable(True)

    tab_bar = self.ui.openRequestTabs.tabBar()
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
  def change_selection(self, index):
    print(f'---------> Changing selection to {index}')
    self.ui.requestGroupsTreeView.selectionModel().setCurrentIndex(
      index,
      QItemSelectionModel.ClearAndSelect
    )

  @Slot()
  def right_click(self, position):
    index = self.ui.requestGroupsTreeView.indexAt(position)

    selected_indexes = self.ui.requestGroupsTreeView.selectionModel().selectedRows()

    if (len(selected_indexes) > 1):
      self.show_multi_selection_context_menu(selected_indexes, position)
    else:
      self.show_single_selection_context_menu(index, position)

  def show_multi_selection_context_menu(self, indexes, position):
    delete_action = QAction(f"Delete {len(indexes)} items")
    delete_action.triggered.connect(lambda: self.multi_delete_clicked(indexes))

    menu = QMenu(self)
    menu.addAction(delete_action)
    menu.exec_(self.ui.requestGroupsTreeView.viewport().mapToGlobal(position))

  def show_single_selection_context_menu(self, index, position):
    tree_item = self.tree_model.getItem(index)

    new_request_action = QAction("New Request")
    new_request_action.triggered.connect(lambda: self.new_request_clicked(index))

    new_dir_action = QAction("New Folder")
    new_dir_action.triggered.connect(lambda: self.new_dir_clicked(index))

    rename_action = QAction("Rename")
    rename_action.triggered.connect(lambda: self.ui.requestGroupsTreeView.edit(index))

    delete_action = QAction("Delete")
    delete_action.triggered.connect(lambda: self.delete_clicked(index))

    menu = QMenu(self)
    if tree_item.is_dir:
      menu.addAction(new_request_action)
      menu.addAction(new_dir_action)

    if index.isValid():
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

  def multi_delete_clicked(self, indexes):
    message_box = QMessageBox()
    message_box.setWindowTitle('PNTest')
    message_box.setText(f'Are you sure you want to delete these {len(indexes)} items?')
    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    message_box.setDefaultButton(QMessageBox.Yes)
    response = message_box.exec_()

    if response == QMessageBox.Yes:
      self.ui.requestGroupsTreeView.selectionModel().clearSelection()

      rows = sorted([i.row() for i in indexes])
      diff = rows[-1] - rows[0]

      self.tree_model.removeRows(rows[0], diff+1, indexes[0].parent())

  # TODO: Most of this method's logic should be in EditorTreeModel, not here.
  def insertChild(self, child_editor_item, parent_index):
    parent_tree_item = self.tree_model.getItem(parent_index)

    if parent_tree_item.editor_item != None:
      child_editor_item.parent_id = parent_tree_item.editor_item.id

    child_editor_item.save()

    child_tree_item = EditorTreeItem.from_editor_item(child_editor_item)
    self.tree_model.insertChild(child_tree_item, parent_index)


    child_index = self.tree_model.index(child_tree_item.childNumber(), 0, parent_index)

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


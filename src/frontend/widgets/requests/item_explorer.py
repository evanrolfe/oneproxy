from PySide2.QtWidgets import QTreeView, QAbstractItemView, QMenu, QMessageBox, QAction
from PySide2.QtCore import QFile, Signal, Slot, Qt, QItemSelectionModel

from models.data.editor_item import EditorItem
from models.qt.editor_tree_model import EditorTreeModel
from models.qt.editor_tree_item import EditorTreeItem

class ItemExplorer(QTreeView):
  item_clicked = Signal(EditorItem)
  item_double_clicked = Signal(EditorItem)

  def __init__(self, *args, **kwargs):
    super(ItemExplorer, self).__init__(*args, **kwargs)

    editor_items = EditorItem.order_by('item_type', 'asc').get()
    self.tree_model = EditorTreeModel('Requests', editor_items)
    self.tree_model.change_selection.connect(self.change_selection)

    self.setModel(self.tree_model)
    self.setDragDropMode(QAbstractItemView.InternalMove)
    self.setSelectionMode(QAbstractItemView.ContiguousSelection)
    self.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.setDragEnabled(True)
    self.setAcceptDrops(True)
    self.setContextMenuPolicy(Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.right_click)
    self.doubleClicked.connect(self.double_click)
    self.clicked.connect(self.click)
    self.setDragDropOverwriteMode(True)

  @Slot()
  def change_selection(self, index):
    print('------------> change_selection called!')
    self.selectionModel().setCurrentIndex(
      index,
      QItemSelectionModel.ClearAndSelect
    )

  @Slot()
  def right_click(self, position):
    index = self.indexAt(position)

    selected_indexes = self.selectionModel().selectedRows()

    if (len(selected_indexes) > 1):
      self.show_multi_selection_context_menu(selected_indexes, position)
    else:
      self.show_single_selection_context_menu(index, position)

  @Slot()
  def double_click(self, index):
    item = self.tree_model.getItem(index)
    if not item.is_dir:
      self.item_double_clicked.emit(item.editor_item)

  @Slot()
  def click(self, index):
    item = self.tree_model.getItem(index)
    print(f'{item.data()}: You clicked me!')
    if not item.is_dir:
      self.item_clicked.emit(item.editor_item)


  def show_multi_selection_context_menu(self, indexes, position):
    delete_action = QAction(f"Delete {len(indexes)} items")
    delete_action.triggered.connect(lambda: self.multi_delete_clicked(indexes))

    menu = QMenu(self)
    menu.addAction(delete_action)
    menu.exec_(self.viewport().mapToGlobal(position))

  def show_single_selection_context_menu(self, index, position):
    tree_item = self.tree_model.getItem(index)

    new_request_action = QAction("New Request")
    new_request_action.triggered.connect(lambda: self.new_request_clicked(index))

    new_dir_action = QAction("New Folder")
    new_dir_action.triggered.connect(lambda: self.new_dir_clicked(index))

    rename_action = QAction("Rename")
    rename_action.triggered.connect(lambda: self.edit(index))

    delete_action = QAction("Delete")
    delete_action.triggered.connect(lambda: self.delete_clicked(index))

    menu = QMenu(self)
    if tree_item.is_dir:
      menu.addAction(new_request_action)
      menu.addAction(new_dir_action)

    if index.isValid():
      menu.addAction(rename_action)
      menu.addAction(delete_action)

    menu.exec_(self.viewport().mapToGlobal(position))

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
      self.selectionModel().clearSelection()

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
    self.selectionModel().setCurrentIndex(
      child_index,
      QItemSelectionModel.ClearAndSelect
    )
    self.edit(child_index)

import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView, QTabBar, QMenu, QAction, QItemDelegate, QMessageBox
from PySide2.QtCore import QFile, Slot, Qt, QItemSelectionModel

from views._compiled.editor.ui_editor_page import Ui_EditorPage

from lib.app_settings import AppSettings
from models.data.editor_item import EditorItem
from models.qt.editor_tree_model import EditorTreeModel
from models.qt.editor_tree_item import EditorTreeItem
from lib.backend import Backend

class EditorPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(EditorPage, self).__init__(*args, **kwargs)

    self.ui = Ui_EditorPage()
    self.ui.setupUi(self)
    self.restore_layout_state()

    self.ui.openRequestTabs.setTabsClosable(True)
    self.ui.openRequestTabs.setMovable(True)

    self.ui.itemExplorer.item_double_clicked.connect(self.open_item)

  def restore_layout_state(self):
    settings = AppSettings.get_instance()
    splitter_state = settings.get("EditorPage.splitter", None)
    self.ui.splitter.restoreState(splitter_state)

  def save_layout_state(self):
    splitter_state = self.ui.splitter.saveState()
    settings = AppSettings.get_instance()
    settings.save("EditorPage.splitter", splitter_state)

    self.ui.requestGroupView.save_layout_state()

  def open_item(self, editor_item):
    print(f'Opening editor item {editor_item.id}')

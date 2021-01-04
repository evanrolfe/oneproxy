import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView, QTabBar, QMenu, QAction, QItemDelegate, QMessageBox
from PySide2.QtCore import QFile, Slot, Qt, QItemSelectionModel

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

    self.ui.openRequestTabs.setTabsClosable(True)
    self.ui.openRequestTabs.setMovable(True)

    self.restore_layout_state()

  def restore_layout_state(self):
    settings = AppSettings.get_instance()
    splitter_state = settings.get("RequestsPage.splitter", None)
    self.ui.splitter.restoreState(splitter_state)

  def save_layout_state(self):
    splitter_state = self.ui.splitter.saveState()
    settings = AppSettings.get_instance()
    settings.save("RequestsPage.splitter", splitter_state)

    self.ui.requestGroupView.save_layout_state()

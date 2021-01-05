import sys

from PySide2.QtWidgets import QApplication, QWidget, QTabWidget
from PySide2.QtCore import Slot

from lib.app_settings import AppSettings
from lib.backend import Backend
from widgets.editor.request_edit_page import RequestEditPage

class Tabs(QTabWidget):
  def __init__(self, *args, **kwargs):
    super(Tabs, self).__init__(*args, **kwargs)

    self.setTabsClosable(True)
    self.setMovable(True)

    self.tabCloseRequested.connect(self.close_tab)

  @Slot()
  def open_item(self, editor_item):
    self.insertTab(self.count(), RequestEditPage(editor_item), editor_item.name)
    self.setCurrentIndex(self.count()-1)

  @Slot()
  def close_tab(self, index):
    self.removeTab(index)

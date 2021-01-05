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
    existing_tab_index = self.get_index_for_editor_item(editor_item)

    if existing_tab_index == None:
      self.insertTab(self.count(), RequestEditPage(editor_item), editor_item.name)
      self.setCurrentIndex(self.count()-1)
    else:
      self.setCurrentIndex(existing_tab_index)

  @Slot()
  def close_tab(self, index):
    self.removeTab(index)

  @Slot()
  def close_item(self, tree_item):
    index = self.get_index_for_editor_item(tree_item.editor_item)
    if index:
      self.removeTab(index)

  @Slot()
  def change_item(self, editor_item):
    index = self.get_index_for_editor_item(editor_item)
    self.setTabText(index, editor_item.name)
    print(f'Changing {editor_item.id} {editor_item.name} in index {index}')

  def get_index_for_editor_item(self, editor_item):
    editor_items = [self.widget(i).editor_item for i in range(0,self.count())]

    try:
      return editor_items.index(editor_item)
    except ValueError:
      return None

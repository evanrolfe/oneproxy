import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.editor.ui_request_group_view import Ui_RequestGroupView

from lib.app_settings import AppSettings
from lib.backend import Backend

class RequestGroupView(QWidget):
  def __init__(self, editor_item):
    super(RequestGroupView, self).__init__()

    self.editor_item = editor_item
    self.ui = Ui_RequestGroupView()
    self.ui.setupUi(self)

    self.ui.urlInput.setText(self.editor_item.name)
    self.layout().setContentsMargins(0, 0, 0, 0)

    self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)
    self.hide_fuzz_table()
    self.settings = AppSettings.get_instance()
    self.restore_layout_state()

  def hide_fuzz_table(self):
    self.ui.fuzzRequestsTable.setVisible(False)
    self.ui.toggleFuzzTableButton.setText(">>")

  @Slot()
  def toggle_fuzz_table(self):
    visible = not self.ui.fuzzRequestsTable.isVisible()
    self.ui.fuzzRequestsTable.setVisible(visible)

    if visible:
      self.restore_layout_state()

    if (visible):
      self.ui.toggleFuzzTableButton.setText("<<")
    else:
      self.ui.toggleFuzzTableButton.setText(">>")

  def restore_layout_state(self):
    splitter_state = self.settings.get("RequestGroupView.splitter", None)
    splitter_state2 = self.settings.get("RequestGroupView.splitter2", None)

    self.ui.splitter.restoreState(splitter_state)
    self.ui.splitter2.restoreState(splitter_state2)

  def save_layout_state(self):
    splitter_state = self.ui.splitter.saveState()
    splitter_state2 = self.ui.splitter2.saveState()

    self.settings.save("RequestGroupView.splitter", splitter_state)
    self.settings.save("RequestGroupView.splitter2", splitter_state2)

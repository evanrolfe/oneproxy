import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from ui_compiled.requests.ui_request_group_view import Ui_RequestGroupView

from lib.backend import Backend

class RequestGroupView(QWidget):
  def __init__(self, *args, **kwargs):
    super(RequestGroupView, self).__init__(*args, **kwargs)

    self.ui = Ui_RequestGroupView()
    self.ui.setupUi(self)

    self.layout().setContentsMargins(0, 0, 0, 0)

    self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)
    self.hide_fuzz_table()

  def hide_fuzz_table(self):
    self.ui.fuzzRequestsTable.setVisible(False)
    self.ui.toggleFuzzTableButton.setText(">>")

  @Slot()
  def toggle_fuzz_table(self):
    visible = not self.ui.fuzzRequestsTable.isVisible()
    self.ui.fuzzRequestsTable.setVisible(visible)

    if (visible):
      self.ui.toggleFuzzTableButton.setText("<<")
    else:
      self.ui.toggleFuzzTableButton.setText(">>")

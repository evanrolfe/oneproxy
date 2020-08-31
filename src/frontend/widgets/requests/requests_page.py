import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from ui_compiled.requests.ui_requests_page import Ui_RequestsPage

from models.backend import Backend

# TODO: Remove the duplication of this between here and request_view.py
TABS_STYLE = """
  QTabWidget::pane {
    margin: 1px 1px 1px 1px;
    padding: -1px;
  }
"""

class RequestsPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(RequestsPage, self).__init__(*args, **kwargs)

    self.ui = Ui_RequestsPage()
    self.ui.setupUi(self)

    self.ui.requestTabs.setStyleSheet(TABS_STYLE)
    self.ui.responseTabs.setStyleSheet(TABS_STYLE)

    self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)

  @Slot()
  def toggle_fuzz_table(self):
    visible = not self.ui.fuzzRequestsTable.isVisible()
    self.ui.fuzzRequestsTable.setVisible(visible)

    if (visible):
      self.ui.toggleFuzzTableButton.setText("<<")
    else:
      self.ui.toggleFuzzTableButton.setText(">>")

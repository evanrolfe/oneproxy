from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot, Qt
from PySide2.QtUiTools import QUiLoader

from views._compiled.editor.ui_request_headers_form import Ui_RequestHeadersForm
from models.qt.editor_request_headers_table_model import EditorRequestHeadersTableModel

class RequestHeadersForm(QWidget):
  DEFAULT_HEADERS = [
    [True, 'Host', '<calculated when request is sent>'],
    [True, 'Content-Length', '<calculated when request is sent>'],
    [True, 'Accept', '*/*']
  ]

  def __init__(self, *args, **kwargs):
    super(RequestHeadersForm, self).__init__(*args, **kwargs)
    self.ui = Ui_RequestHeadersForm()
    self.ui.setupUi(self)

    self.headers = self.DEFAULT_HEADERS[:]
    self.table_model = EditorRequestHeadersTableModel(self.headers)
    self.ui.headersTable.setModel(self.table_model)

    horizontalHeader = self.ui.headersTable.horizontalHeader()
    horizontalHeader.setStretchLastSection(True)
    horizontalHeader.setSectionResizeMode(QHeaderView.Interactive)

    self.ui.headersTable.setColumnWidth(0, 20)
    self.ui.headersTable.setColumnWidth(1, 250)

    self.ui.showGeneratedHeaders.setTristate(False)
    self.ui.showGeneratedHeaders.stateChanged.connect(self.show_generated_headers)

  @Slot()
  def show_generated_headers(self, state):
    print(self.table_model.get_headers())

    if state == Qt.Checked:
      self.ui.headersTable.showRow(0)
      self.ui.headersTable.showRow(1)
    else:
      self.ui.headersTable.hideRow(0)
      self.ui.headersTable.hideRow(1)


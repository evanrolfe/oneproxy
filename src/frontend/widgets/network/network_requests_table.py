import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Qt, Slot, Signal, QItemSelection
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery

from ui_compiled.network.ui_network_requests_table import Ui_NetworkRequestsTable

class NetworkRequestsTable(QWidget):
  request_selected = Signal(QItemSelection, QItemSelection)

  def __init__(self, *args, **kwargs):
    super(NetworkRequestsTable, self).__init__(*args, **kwargs)
    self.ui = Ui_NetworkRequestsTable()
    self.ui.setupUi(self)

    horizontalHeader = self.ui.requestsTable.horizontalHeader()
    horizontalHeader.setStretchLastSection(True)
    horizontalHeader.setSectionResizeMode(QHeaderView.Interactive)
    horizontalHeader.setSortIndicator(0, Qt.DescendingOrder)
    self.ui.requestsTable.setSortingEnabled(True)

    verticalHeader = self.ui.requestsTable.verticalHeader()
    verticalHeader.setSectionResizeMode(QHeaderView.Fixed)
    verticalHeader.setDefaultSectionSize(20)
    verticalHeader.setVisible(False)

    # Set row selection behaviour:
    self.ui.requestsTable.setSelectionBehavior(QAbstractItemView.SelectRows)

  def setTableModel(self, model):
    self.ui.requestsTable.setModel(model)

    # Request Selected Signal:
    self.ui.requestsTable.selectionModel().selectionChanged.connect(self.request_selected)

    self.ui.requestsTable.setColumnWidth(0, 50)
    self.ui.requestsTable.setColumnWidth(1, 60)
    self.ui.requestsTable.setColumnWidth(2, 60)
    self.ui.requestsTable.setColumnWidth(3, 150)
    self.ui.requestsTable.setColumnWidth(4, 300)
    self.ui.requestsTable.setColumnWidth(5, 50)
    self.ui.requestsTable.setColumnWidth(6, 70)

import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView, QMenu, QAction
from PySide2.QtCore import QFile, Qt, Slot, Signal, QItemSelection
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery

from ui_compiled.network.ui_network_requests_table import Ui_NetworkRequestsTable
from widgets.network.network_display_filters import NetworkDisplayFilters
from widgets.network.network_capture_filters import NetworkCaptureFilters

class NetworkRequestsTable(QWidget):
  request_selected = Signal(QItemSelection, QItemSelection)
  delete_requests = Signal(list)

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

    # Display & Capture Filters:
    self.network_display_filters = NetworkDisplayFilters(self)
    self.network_capture_filters = NetworkCaptureFilters(self)
    self.ui.displayFiltersButton.clicked.connect(lambda: self.network_display_filters.show())
    self.ui.captureFiltersButton.clicked.connect(lambda: self.network_capture_filters.show())

    # Set row selection behaviour:
    self.ui.requestsTable.setSelectionBehavior(QAbstractItemView.SelectRows)

    # Set right-click behaviour:
    self.ui.requestsTable.setContextMenuPolicy(Qt.CustomContextMenu)
    self.ui.requestsTable.customContextMenuRequested.connect(self.right_clicked)
    self.selected_request_ids = []

  def setTableModel(self, model):
    self.table_model = model
    self.ui.requestsTable.setModel(model)

    # Request Selected Signal:
    self.ui.requestsTable.selectionModel().selectionChanged.connect(self.request_selected)
    self.ui.requestsTable.selectionModel().selectionChanged.connect(self.set_selected_requests)

    self.ui.requestsTable.setColumnWidth(0, 50)
    self.ui.requestsTable.setColumnWidth(1, 60)
    self.ui.requestsTable.setColumnWidth(2, 60)
    self.ui.requestsTable.setColumnWidth(3, 150)
    self.ui.requestsTable.setColumnWidth(4, 300)
    self.ui.requestsTable.setColumnWidth(5, 50)
    self.ui.requestsTable.setColumnWidth(6, 70)

  @Slot()
  def set_selected_requests(self, selected, deselected):
    selected_q_indexes = self.ui.requestsTable.selectionModel().selectedRows()
    self.selected_request_ids = list(map(lambda index: index.data(), selected_q_indexes))

  @Slot()
  def right_clicked(self, position):
    index = self.ui.requestsTable.indexAt(position)
    request = self.table_model.request_data.requests[index.row()]

    menu = QMenu()

    if (len(self.selected_request_ids) > 1):
      action = QAction(f"Delete {len(self.selected_request_ids)} selected requests")
      menu.addAction(action)
      action.triggered.connect(lambda: self.delete_requests.emit(self.selected_request_ids))

    else:
      action = QAction("Delete request")
      menu.addAction(action)
      action.triggered.connect(lambda: self.delete_requests.emit([request.id]))

    global_position = self.sender().mapToGlobal(position)
    menu.exec_(global_position)

  @Slot()
  def display_filters_clicked(self):
    print("You clicked me!")

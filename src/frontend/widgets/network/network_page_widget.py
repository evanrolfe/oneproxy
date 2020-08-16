import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery

from ui_compiled.network.ui_network_page_widget import Ui_NetworkPageWidget

from models.requests_table_model import RequestsTableModel
from models.request_data import RequestData

class NetworkPageWidget(QWidget):
  def __init__(self, *args, **kwargs):
    super(NetworkPageWidget, self).__init__(*args, **kwargs)
    self.ui = Ui_NetworkPageWidget()
    self.ui.setupUi(self)

    # Setup the request model
    self.request_data = RequestData()
    self.request_data.load_requests()
    self.requests_table_model = RequestsTableModel(self.request_data)

    self.ui.requestsTableWidget.setTableModel(self.requests_table_model)
    self.ui.requestsTableWidget.request_selected.connect(self.select_request)
    self.ui.requestsTableWidget.delete_requests.connect(self.delete_requests)

    #self.ui.splitter.layout().setContentsMargins(0, 0, 0, 0)
    #self.ui.layout().setContentsMargins(0, 0, 0, 0)
    #self.ui.splitter.layout().setContentsMargins(0, 0, 0, 0)
    #self.ui.splitter.setStyleSheet("padding: 0px;")
    #self.ui.splitter.setSpacing(0)

  @Slot()
  def select_request(self, selected, deselected):
    if (len(selected.indexes()) > 0):
      selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
      selected_id = selected_id_cols[0].data()
      #print(f"SELECTING ID: {selected_id}")
      request = self.request_data.load_request(selected_id)
      self.ui.requestViewWidget.set_request(request)

  @Slot()
  def delete_requests(self, request_ids):
    self.requests_table_model.delete_requests(request_ids)


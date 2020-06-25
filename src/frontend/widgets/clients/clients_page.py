import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from ui_compiled.clients.ui_clients_page import Ui_ClientsPage

from models.backend import Backend
from models.clients_table_model import ClientsTableModel
from models.client_data import ClientData

class ClientsPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(ClientsPage, self).__init__(*args, **kwargs)
    self.ui = Ui_ClientsPage()
    self.ui.setupUi(self)

    # Setup the client model
    self.client_data = ClientData()
    self.client_data.load_clients()
    self.clients_table_model = ClientsTableModel(self.client_data)

    self.ui.clientsTable.setTableModel(self.clients_table_model)
    self.ui.clientsTable.client_selected.connect(self.select_client)

    # Reload when the clients have changed:
    self.backend = Backend.get_instance()
    self.backend.register_callback('clientsChanged', self.clients_table_model.reload_data)

  def showEvent(self, event):
    self.clients_table_model.reload_data()

  @Slot()
  def select_client(self, selected, deselected):
    selected_id = selected.indexes()[0].data()
    client = self.client_data.load_client(selected_id)
    #self.ui.clientView.setClient(client)

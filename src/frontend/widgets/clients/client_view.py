import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from ui_compiled.clients.ui_client_view import Ui_ClientView

class ClientView(QWidget):
  def __init__(self, *args, **kwargs):
    super(ClientView, self).__init__(*args, **kwargs)
    self.ui = Ui_ClientView()
    self.ui.setupUi(self)

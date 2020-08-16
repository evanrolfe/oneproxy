import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon

from ui_compiled.network.ui_network_capture_filters import Ui_NetworkCaptureFilters

from models.backend import Backend

class NetworkCaptureFilters(QDialog):
  def __init__(self, parent = None):
    super(NetworkCaptureFilters, self).__init__(parent)

    self.ui = Ui_NetworkCaptureFilters()
    self.ui.setupUi(self)
    self.setModal(True)

  #def showEvent(self, event):
    # print("NewClientModal - showEvent")
    # self.backend.get_available_clients()

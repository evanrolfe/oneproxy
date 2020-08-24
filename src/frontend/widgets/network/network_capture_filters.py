import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon

from ui_compiled.network.ui_network_capture_filters import Ui_NetworkCaptureFilters
from models.capture_filters_data import CaptureFiltersData

from models.backend import Backend

class NetworkCaptureFilters(QDialog):
  def __init__(self, parent = None):
    super(NetworkCaptureFilters, self).__init__(parent)

    self.ui = Ui_NetworkCaptureFilters()
    self.ui.setupUi(self)
    self.setModal(True)

    self.ui.cancelButton.clicked.connect(self.close)
    self.ui.saveButton.clicked.connect(self.save)
    self.ui.hostSettingDropdown.currentIndexChanged.connect(self.host_setting_changed)
    self.ui.pathSettingDropdown.currentIndexChanged.connect(self.path_setting_changed)

    self.load_capture_filters()

  def showEvent(self, event):
    self.load_capture_filters()

  def load_capture_filters(self):
    print("Loading capture filters")
    self.capture_filters = CaptureFiltersData.load()

    host_index = self.setting_to_index(self.capture_filters.host_setting)
    self.ui.hostSettingDropdown.setCurrentIndex(host_index)

    path_index = self.setting_to_index(self.capture_filters.path_setting)
    self.ui.pathSettingDropdown.setCurrentIndex(path_index)

    self.ui.hostsText.setPlainText("\n".join(self.capture_filters.host_list))
    self.ui.pathsText.setPlainText("\n".join(self.capture_filters.path_list))

  @Slot()
  def save(self):
    #self.backend.send_command(self.launch_command)
    hosts_list = self.ui.hostsText.toPlainText()
    hosts_setting_index = self.ui.hostSettingDropdown.currentIndex()
    hosts_setting = 'include' if (hosts_setting_index == 0) else 'exclude'

    paths_list = self.ui.pathsText.toPlainText()
    paths_setting_index = self.ui.pathSettingDropdown.currentIndex()
    paths_setting = 'include' if (paths_setting_index == 0) else 'exclude'

    # TODO: Save to the database

    self.close()

  @Slot()
  def host_setting_changed(self, index):
    self.ui.hostsText.setDisabled((index == 0))

  @Slot()
  def path_setting_changed(self, index):
    self.ui.pathsText.setDisabled((index == 0))

  def setting_to_index(self, setting):
    if setting == '':
      return 0
    elif setting == 'include':
      return 1
    elif setting == 'exclude':
      return 2

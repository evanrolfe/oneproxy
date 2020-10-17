import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon

from ui_compiled.crawls.ui_new_crawl import Ui_NewCrawl

from models.backend import Backend
from models.client_data import ClientData

class NewCrawl(QDialog):
  def __init__(self, parent = None):
    super(NewCrawl, self).__init__(parent)

    self.ui = Ui_NewCrawl()
    self.ui.setupUi(self)
    self.setModal(True)

    self.ui.cancelButton.clicked.connect(self.close)
    self.ui.saveButton.clicked.connect(self.start)

    self.load_clients()

  def showEvent(self, event):
    self.load_clients()

  def load_clients(self):
    print("Loading clients")

    self.client_data = ClientData()
    self.client_data.load_browsers()

    self.ui.clientsDropdown.clear()

    for client in self.client_data.clients:
      self.ui.clientsDropdown.addItem(client.title, client.id)

  @Slot()
  def start(self):
    print("Saving")
    client_id = self.ui.clientsDropdown.itemData(self.ui.clientsDropdown.currentIndex())
    browser_mode = (self.ui.browserModeDropdown.currentIndex() == 0)
    base_url = self.ui.baseURLText.text()
    ignore_urls = self.ui.ignoreURLsText.toPlainText().split("\n")

    max_concurrency = int(self.ui.maxConcurrencyText.text())
    max_depth = int(self.ui.maxDepthText.text())
    xhr_timeout = int(self.ui.xhrTimeoutText.text())
    wait_for_page = int(self.ui.waitPageText.text())
    verbose = (self.ui.logLevelDropdown.currentIndex() == 1)

    print(client_id)
    print(browser_mode)
    print(base_url)
    print(ignore_urls)
    print(max_concurrency)
    print(max_depth)
    print(xhr_timeout)
    print(wait_for_page)
    print(verbose)

import sys
import json
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog
from PySide2.QtCore import Slot, Signal
from PySide2.QtGui import QIcon

from ui_compiled.crawls.ui_new_crawl import Ui_NewCrawl

from models.backend import Backend
from models.client_data import ClientData
from models.crawl_data import CrawlData
from models.crawl import Crawl

class NewCrawl(QDialog):
  crawl_saved = Signal()

  def __init__(self, parent = None):
    super(NewCrawl, self).__init__(parent)

    self.ui = Ui_NewCrawl()
    self.ui.setupUi(self)
    self.setModal(True)

    self.backend = Backend.get_instance()

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
    headless = (self.ui.browserModeDropdown.currentIndex() == 0)
    base_url = self.ui.baseURLText.text()
    ignore_urls = self.ui.ignoreURLsText.toPlainText().split("\n")
    ignore_urls = list(filter(lambda url: not url == '', ignore_urls))

    max_concurrency = int(self.ui.maxConcurrencyText.text())
    max_depth = int(self.ui.maxDepthText.text())
    xhr_timeout = int(self.ui.xhrTimeoutText.text()) * 1000
    wait_for_page = int(self.ui.waitPageText.text()) * 1000
    verbose = (self.ui.logLevelDropdown.currentIndex() == 1)

    config = {
        "baseUrl": base_url,
        "clickButtons": False,
        "maxConcurrency": max_concurrency,
        "maxDepth": max_depth,
        "xhrTimeout": xhr_timeout,
        "waitOnEachPage": wait_for_page,
        "verboseOutput": verbose,
        "headless": headless,
        "ignoreLinksIncluding": ignore_urls
    }

    crawl = Crawl({
      "client_id": client_id,
      "status": "created",
      "config": json.dumps(config)
    })

    result = CrawlData.save(crawl)
    self.crawl_saved.emit()
    self.backend.start_crawler(crawl.id)
    self.close()

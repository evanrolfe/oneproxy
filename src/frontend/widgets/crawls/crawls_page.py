import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from ui_compiled.crawls.ui_crawls_page import Ui_CrawlsPage

from widgets.crawls.new_crawl import NewCrawl
from models.backend import Backend
from models.crawls_table_model import CrawlsTableModel
from models.crawl_data import CrawlData

class CrawlsPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(CrawlsPage, self).__init__(*args, **kwargs)
    self.ui = Ui_CrawlsPage()
    self.ui.setupUi(self)

    # Setup the crawl model
    self.crawl_data = CrawlData()
    self.crawl_data.load_crawls()
    self.crawls_table_model = CrawlsTableModel(self.crawl_data)

    self.ui.crawlsTable.setTableModel(self.crawls_table_model)
    self.ui.crawlsTable.crawl_selected.connect(self.select_crawl)

    # Reload when the crawls have changed:
    self.backend = Backend.get_instance()

    # New Crawler Dialog:
    self.new_crawl = NewCrawl(self)
    self.new_crawl.crawl_saved.connect(self.reload_crawls)
    self.ui.newCrawlerButton.clicked.connect(lambda: self.new_crawl.show())

  def showEvent(self, event):
    self.reload_crawls()

  @Slot()
  def reload_crawls(self):
    print("Reloading crawls!")
    self.crawls_table_model.reload_data()

  @Slot()
  def select_crawl(self, selected, deselected):
    selected_id = selected.indexes()[0].data()
    crawl = self.crawl_data.load_crawl(selected_id)
    self.ui.crawlView.set_crawl(crawl)

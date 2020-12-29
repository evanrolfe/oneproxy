import sys
import pathlib
import asyncio

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QHeaderView, QAbstractItemView, QStackedWidget, QToolButton, QAction, QMenu, QShortcut, QListWidgetItem, QListView
from PySide2.QtCore import QFile, Qt, QTextStream, QResource, SIGNAL, Slot, QPoint, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtGui import QIcon, QKeySequence

from ui_compiled.ui_main_window import Ui_MainWindow
from models.requests_table_model import RequestsTableModel
from widgets.network.network_page_widget import NetworkPageWidget
from widgets.intercept.intercept_page import InterceptPage
from widgets.clients.clients_page import ClientsPage
from widgets.crawls.crawls_page import CrawlsPage
from widgets.requests.requests_page import RequestsPage
from widgets.new_client_modal import NewClientModal

# pyside2-rcc assets/assets.qrc > assets_compiled/assets.py
import assets_compiled.assets

# Makes CTRL+C close the app:
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

sidebar_style = """
QListWidget {
  background: #E9E9E9;
}

QListWidget::item {
  padding: 5px;
}

QListWidget::item::!selected {
  border-left: 2px solid #E9E9E9;
}

QListWidget::item::selected {
  border-left: 2px solid #82b9bc;
}
"""

class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.setWindowTitle('OneProxy')
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # TOGGLE TOOLBAR HERE:
    #self.setup_toolbar()
    self.ui.toolBar.setVisible(False)

    # Setup pages:
    self.network_page_widget = NetworkPageWidget()
    self.intercept_page = InterceptPage()
    self.clients_page = ClientsPage()
    self.crawls_page = CrawlsPage()
    self.requests_page = RequestsPage()

    # Setup stacked widget:
    self.ui.stackedWidget.addWidget(self.network_page_widget)
    self.ui.stackedWidget.addWidget(self.intercept_page)
    self.ui.stackedWidget.addWidget(self.clients_page)
    self.ui.stackedWidget.addWidget(self.crawls_page)
    self.ui.stackedWidget.addWidget(self.requests_page)
    self.ui.stackedWidget.setCurrentWidget(self.network_page_widget)

    # Set padding on widgets:
    self.ui.centralWidget.layout().setContentsMargins(0, 0, 0, 0)
    self.network_page_widget.layout().setContentsMargins(0, 4, 0, 0)
    self.clients_page.layout().setContentsMargins(0, 0, 0, 0)
    self.crawls_page.layout().setContentsMargins(0, 0, 4, 0)
    self.intercept_page.layout().setContentsMargins(0, 4, 0, 0)
    self.requests_page.layout().setContentsMargins(0, 0, 0, 0)

    # Add actions to sidebar:
    self.setup_sidebar()

    # Shortcut for closing app:
    self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C), self), SIGNAL('activated()'), self.exit)

    # Create new client modal
    self.new_client_modal = NewClientModal(self)

  def set_backend(self, backend):
    self.backend = backend

  @Slot()
  def about_to_quit(self):
    self.backend.kill()

  def exit(self):
    QApplication.quit()

  def setup_toolbar(self):
    openProjectButton = QToolButton()

    # New project button:
    newProjectButton = QToolButton()
    newProjectButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

    newProjectaction = QAction()
    newProjectaction.setIcon(QIcon(":/icons/icons8-add-folder-80.png"))
    newProjectaction.setText("New Project")
    newProjectButton.setDefaultAction(newProjectaction)

    # Open project actions in toolbar:
    openProjectButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    openProjectaction = QAction()
    openProjectaction.setIcon(QIcon("://icons/icons8-opened-folder-80.png"))
    openProjectaction.setText("Open Project")
    openProjectButton.setDefaultAction(openProjectaction)

    # New client button in toolbar:
    newClientButton = QToolButton()
    newClientButton.setPopupMode(QToolButton.InstantPopup)
    newClientButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    newClientaction = QAction()
    newClientaction.setIcon(QIcon("://icons/icons8-add-property-80.png"))
    newClientaction.setText("New Client")
    newClientButton.setDefaultAction(newClientaction)
    newClientButton.triggered.connect(self.new_client_click)

    self.ui.toolBar.addWidget(newProjectButton)
    self.ui.toolBar.addWidget(openProjectButton)
    self.ui.toolBar.addWidget(newClientButton)

  def setup_sidebar(self):
    self.ui.sideBar.currentItemChanged.connect(self.sidebar_item_clicked)

    self.ui.sideBar.setViewMode(QListView.IconMode)
    self.ui.sideBar.setFlow(QListView.TopToBottom)
    self.ui.sideBar.setStyleSheet(sidebar_style)
    self.ui.sideBar.setMovement(QListView.Static)
    self.ui.sideBar.setUniformItemSizes(True)
    #icon_size = QSize(52, 35)

    # Network Item
    network_item = QListWidgetItem(QIcon(":/icons/icons8-cloud-backup-restore-50.png"), None)
    network_item.setData(Qt.UserRole, 'network')
    #network_item.setSizeHint(icon_size)
    self.ui.sideBar.addItem(network_item)

    # Intercept Item
    intercept_item = QListWidgetItem(QIcon(":/icons/icons8-rich-text-converter-50.png"), None)
    intercept_item.setData(Qt.UserRole, 'intercept')
    self.ui.sideBar.addItem(intercept_item)

    # Clients Item
    clients_item = QListWidgetItem(QIcon(":/icons/icons8-browse-page-50.png"), None)
    clients_item.setData(Qt.UserRole, 'clients')
    self.ui.sideBar.addItem(clients_item)

    # Requests Item
    requests_item = QListWidgetItem(QIcon(":/icons/icons8-compose-50.png"), None)
    requests_item.setData(Qt.UserRole, 'requests')
    self.ui.sideBar.addItem(QListWidgetItem(requests_item))

    # Crawler Item
    crawler_item = QListWidgetItem(QIcon(":/icons/icons8-spiderweb-50.png"), None)
    crawler_item.setData(Qt.UserRole, 'crawler')
    self.ui.sideBar.addItem(crawler_item)

    # Extensions Item
    extensions_item = QListWidgetItem(QIcon(":/icons/icons8-plus-math-50.png"), None)
    extensions_item.setData(Qt.UserRole, 'extensions')
    self.ui.sideBar.addItem(extensions_item)

    self.ui.sideBar.setCurrentRow(0)

  @Slot()
  def new_client_click(self):
    self.new_client_modal.show()

  @Slot()
  def sidebar_item_clicked(self, item):
    item_value = item.data(Qt.UserRole)

    if item_value == 'network':
      self.ui.stackedWidget.setCurrentWidget(self.network_page_widget)
    elif item_value == 'intercept':
      self.ui.stackedWidget.setCurrentWidget(self.intercept_page)
    elif item_value == 'clients':
      self.ui.stackedWidget.setCurrentWidget(self.clients_page)
    elif item_value == 'crawler':
      self.ui.stackedWidget.setCurrentWidget(self.crawls_page)
    elif item_value == 'requests':
      self.ui.stackedWidget.setCurrentWidget(self.requests_page)

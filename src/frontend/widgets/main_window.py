import sys
import pathlib

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QHeaderView, QAbstractItemView, QStackedWidget, QToolButton, QAction, QMenu, QShortcut, QListWidgetItem
from PySide2.QtCore import QFile, Qt, QTextStream, QResource, SIGNAL, Slot, QPoint
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtGui import QIcon, QKeySequence

from ui_compiled.ui_main_window import Ui_MainWindow
from models.backend import Backend
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

class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.app_path = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
    print(f'[Frontend] App path: {self.app_path}')

    # Start the backend
    Backend(self.app_path)
    self.backend = Backend.get_instance()

    self.setWindowTitle('OneProxy')
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.setup_toolbar()
    self.load_database()

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
    self.ui.sideBar.addItem(QListWidgetItem("Network"))
    self.ui.sideBar.addItem(QListWidgetItem("Intercept"))
    self.ui.sideBar.addItem(QListWidgetItem("Clients"))
    self.ui.sideBar.addItem(QListWidgetItem("Requests"))
    self.ui.sideBar.addItem(QListWidgetItem("Crawler"))
    self.ui.sideBar.itemClicked.connect(self.sidebar_item_clicked)

    # Shortcut for closing app:
    self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C), self), SIGNAL('activated()'), self.exit)

    # Create new client modal
    self.new_client_modal = NewClientModal(self)

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

  def load_database(self):
    db_path = f'{self.app_path}/tmp/production.db'
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_path)
    db_result = db.open()

    if db_result == True:
      print(f'[Frontend] Loaded database from {db_path}')
    else:
      print(f'[Frontend] ERROR could not load database from {db_path}')

  @Slot()
  def new_client_click(self):
    self.new_client_modal.show()

  @Slot()
  def sidebar_item_clicked(self, item):
    text = item.text().lower()

    if text == 'network':
      self.ui.stackedWidget.setCurrentWidget(self.network_page_widget)
    elif text == 'intercept':
      self.ui.stackedWidget.setCurrentWidget(self.intercept_page)
    elif text == 'clients':
      self.ui.stackedWidget.setCurrentWidget(self.clients_page)
    elif text == 'crawler':
      self.ui.stackedWidget.setCurrentWidget(self.crawls_page)
    elif text == 'requests':
      self.ui.stackedWidget.setCurrentWidget(self.requests_page)

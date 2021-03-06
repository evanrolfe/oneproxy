import sys
import pathlib
import asyncio

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QHeaderView, QAbstractItemView, QStackedWidget, QToolButton, QAction, QMenu, QShortcut, QListWidgetItem, QListView
from PySide2.QtCore import QFile, Qt, QTextStream, QResource, SIGNAL, Slot, QPoint, QSize, QSettings, Signal
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtGui import QIcon, QKeySequence

from views._compiled.ui_main_window import Ui_MainWindow

from lib.app_settings import AppSettings
from widgets.network.network_page_widget import NetworkPageWidget
from widgets.intercept.intercept_page import InterceptPage
from widgets.clients.clients_page import ClientsPage
from widgets.crawls.crawls_page import CrawlsPage
from widgets.editor.editor_page import EditorPage

# pyside2-rcc assets/assets.qrc > assets_compiled/assets.py
import assets._compiled.assets

# Makes CTRL+C close the app:
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

#   background: #E9E9E9;
sidebar_style = """
QListWidget#sideBar {
  background: #3F3F3F;
}

QListWidget::item#sideBar {
  padding: 5px;
}

QListWidget::item::!selected#sideBar {
  border-left: 2px solid #3F3F3F;
}

QListWidget::item::selected#sideBar {
  border-left: 2px solid #2A82DA;
}
"""

class MainWindow(QMainWindow):
  reload_style = Signal()

  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.setWindowTitle('OneProxy')
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.toolBar.setVisible(False)

    # Setup pages:
    self.network_page_widget = NetworkPageWidget()
    self.intercept_page = InterceptPage()
    self.clients_page = ClientsPage()
    self.crawls_page = CrawlsPage()
    self.editor_page = EditorPage()

    # Setup stacked widget:
    self.ui.stackedWidget.addWidget(self.network_page_widget)
    self.ui.stackedWidget.addWidget(self.intercept_page)
    self.ui.stackedWidget.addWidget(self.clients_page)
    self.ui.stackedWidget.addWidget(self.crawls_page)
    self.ui.stackedWidget.addWidget(self.editor_page)
    self.ui.stackedWidget.setCurrentWidget(self.network_page_widget)

    # Set padding on widgets:
    self.ui.centralWidget.layout().setContentsMargins(0, 0, 0, 0)
    self.ui.stackedWidget.setContentsMargins(0, 0, 0, 0)

    margins = [0, 0, 0, 0]
    self.network_page_widget.layout().setContentsMargins(*margins)
    self.clients_page.layout().setContentsMargins(*margins)
    self.crawls_page.layout().setContentsMargins(*margins)
    self.intercept_page.layout().setContentsMargins(*margins)
    self.editor_page.layout().setContentsMargins(*margins)

    # Add actions to sidebar:
    self.setup_sidebar()

    # Shortcut for closing app:
    self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C), self), SIGNAL('activated()'), self.exit)
    self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self), SIGNAL('activated()'), self.reload_style)

    self.network_page_widget.send_request_to_editor.connect(self.editor_page.send_request_to_editor)
    self.network_page_widget.send_request_to_editor.connect(self.show_editor_page)

    # Menubar:
    menu_bar = self.menuBar()
    menu_bar.setNativeMenuBar(True)

    self.restore_layout_state()
    self.show_editor_page()

  def set_backend(self, backend):
    self.backend = backend

  def restore_layout_state(self):
    settings = AppSettings.get_instance()
    geometry = settings.get('geometry', None)

    if (geometry != None):
      self.restoreGeometry(geometry)

  def save_layout_state(self):
    geometry = self.saveGeometry()

    settings = AppSettings.get_instance()
    settings.save('geometry', geometry)

  @Slot()
  def reload_style(self):
    file = QFile('/home/evan/Code/oneproxy/src/frontend/assets/style/dark2.qss')
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    self.setStyleSheet(stream.readAll())

    print('reloaded the stylesheet!')

  @Slot()
  def show_editor_page(self):
    self.ui.sideBar.setCurrentRow(3)
    self.ui.stackedWidget.setCurrentWidget(self.editor_page)

  @Slot()
  def about_to_quit(self):
    self.save_layout_state()
    self.network_page_widget.save_layout_state()
    self.editor_page.save_layout_state()
    self.backend.kill()

  def exit(self):
    QApplication.quit()

  def setup_sidebar(self):
    self.ui.sideBar.currentItemChanged.connect(self.sidebar_item_clicked)

    self.ui.sideBar.setObjectName('sideBar')

    self.ui.sideBar.setViewMode(QListView.IconMode)
    self.ui.sideBar.setFlow(QListView.TopToBottom)
    self.ui.sideBar.setMovement(QListView.Static)
    self.ui.sideBar.setUniformItemSizes(True)
    #icon_size = QSize(52, 35)

    # Network Item
    network_item = QListWidgetItem(QIcon(":/icons/dark/icons8-cloud-backup-restore-50.png"), None)
    network_item.setData(Qt.UserRole, 'network')
    #network_item.setSizeHint(icon_size)
    self.ui.sideBar.addItem(network_item)

    # Intercept Item
    intercept_item = QListWidgetItem(QIcon(":/icons/dark/icons8-rich-text-converter-50.png"), None)
    intercept_item.setData(Qt.UserRole, 'intercept')
    self.ui.sideBar.addItem(intercept_item)

    # Clients Item
    clients_item = QListWidgetItem(QIcon(":/icons/dark/icons8-browse-page-50.png"), None)
    clients_item.setData(Qt.UserRole, 'clients')
    self.ui.sideBar.addItem(clients_item)

    # Requests Item
    requests_item = QListWidgetItem(QIcon(":/icons/dark/icons8-compose-50.png"), None)
    requests_item.setData(Qt.UserRole, 'requests')
    self.ui.sideBar.addItem(QListWidgetItem(requests_item))

    # Crawler Item
    crawler_item = QListWidgetItem(QIcon(":/icons/dark/icons8-spiderweb-50.png"), None)
    crawler_item.setData(Qt.UserRole, 'crawler')
    self.ui.sideBar.addItem(crawler_item)

    # Extensions Item
    extensions_item = QListWidgetItem(QIcon(":/icons/dark/icons8-plus-math-50.png"), None)
    extensions_item.setData(Qt.UserRole, 'extensions')
    self.ui.sideBar.addItem(extensions_item)

    self.ui.sideBar.setCurrentRow(0)

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
      self.ui.stackedWidget.setCurrentWidget(self.editor_page)

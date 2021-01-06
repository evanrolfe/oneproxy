import sys
import traceback
import pathlib

from PySide2.QtWidgets import QApplication, QLabel, QStyleFactory
from PySide2.QtCore import QFile, QTextStream, Qt, QCoreApplication, QSettings
from PySide2.QtGui import QPalette, QColor

from lib.backend import Backend
from lib.database import Database
from lib.palettes import Palettes
from widgets.main_window import MainWindow

THEME = 'light'
LIGHT_STYLE = """
QTabWidget::pane {
  margin: 1px 1px 1px 1px;
  padding: -1px;
}
"""

def excepthook(type, value, tb):
  # TODO: Only close the backend if the exception is fatal
  backend = Backend.get_instance()
  backend.kill()

  print("----------------------------------------------------------")
  traceback_details = '\n'.join(traceback.extract_tb(tb).format())
  print(f"Type: {type}\nValue: {value}\nTraceback: {traceback_details}")

sys.excepthook = excepthook

if __name__ == "__main__":

  app = QApplication(sys.argv)

  # Setup stylesheet:
  #file = QFile('/home/evan/Code/oneproxypy/assets/style.qss')
  #file.open(QFile.ReadOnly | QFile.Text)
  #stream = QTextStream(file)
  #app.setStyleSheet(stream.readAll())

  app_path = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
  db_path = '/home/evan/Desktop/oneproxy.db'

  print(f'[Frontend] App path: {app_path}')
  print(f'[Frontend] DB path: {db_path}')

  database = Database(db_path)
  database.load_or_create()

  backend = Backend(app_path, db_path)
  backend.register_callback('backendLoaded', lambda: print('Backend Loaded!'))
  backend.start()

  main_window = MainWindow()
  main_window.set_backend(backend)
  main_window.show()

  app.aboutToQuit.connect(main_window.about_to_quit)

  # Settings:
  QCoreApplication.setOrganizationName('PnTLimted')
  QCoreApplication.setOrganizationDomain('getpntest.com')
  QCoreApplication.setApplicationName('PnTest')

  # Style:
  app.setStyle('Fusion')

  if (THEME == 'light'):
    app.setStyleSheet(LIGHT_STYLE)
  elif (THEME == 'dark'):
    app.setPalette(Palettes.dark())

  sys.exit(app.exec_())

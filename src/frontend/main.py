import sys
import traceback
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtCore import QFile, QTextStream

from models.backend import Backend
from widgets.main_window import MainWindow

def excepthook(type, value, tb):
    backend = Backend.get_instance()
    backend.kill()

    print("----------------------------------------------------------")
    traceback_details = '\n'.join(traceback.extract_tb(tb).format())
    print(f"Type: {type}\nValue: {value}\nTraceback: {traceback_details}")

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Setup stylesheet:
    # file = QFile('/home/evan/Code/oneproxypy/assets/style/dark.qss')
    # file.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(file)
    # app.setStyleSheet(stream.readAll())

    main_window = MainWindow()
    main_window.show()

    app.aboutToQuit.connect(main_window.about_to_quit)

    sys.exit(app.exec_())

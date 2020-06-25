import sys
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtCore import QFile, QTextStream

from widgets.main_window import MainWindow

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

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.editor.ui_request_body_form import Ui_RequestBodyForm

class RequestBodyForm(QWidget):
  def __init__(self, *args, **kwargs):
    super(RequestBodyForm, self).__init__(*args, **kwargs)
    self.ui = Ui_RequestBodyForm()
    self.ui.setupUi(self)

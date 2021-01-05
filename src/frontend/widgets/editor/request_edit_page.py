import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.editor.ui_request_edit_page import Ui_RequestEditPage

from lib.app_settings import AppSettings
from lib.backend import Backend

class RequestEditPage(QWidget):
  METHODS = ['GET','POST','PATCH','PUT','DELETE']

  def __init__(self, editor_item):
    super(RequestEditPage, self).__init__()

    self.editor_item = editor_item
    self.request = self.editor_item.item()
    self.ui = Ui_RequestEditPage()
    self.ui.setupUi(self)

    self.ui.urlInput.setText(self.editor_item.name)
    self.layout().setContentsMargins(0, 0, 0, 0)

    self.hide_fuzz_table()
    self.settings = AppSettings.get_instance()
    self.restore_layout_state()

    self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)
    self.ui.saveButton.clicked.connect(self.save_request)
    self.ui.methodInput.insertItems(0, self.METHODS)
    self.show_request()
    self.modified = False

    # Form inputs:
    self.ui.urlInput.textChanged.connect(lambda text: self.form_field_changed('url', text))
    self.ui.methodInput.currentIndexChanged.connect(lambda index: self.form_field_changed('method', self.METHODS[index]))

  def show_request(self):
    self.ui.urlInput.setText(self.request.url)
    self.set_method_on_form(self.request.method)

  @Slot()
  def save_request(self):
    method = self.ui.methodInput.currentText()
    url = self.ui.urlInput.text()

    self.request.url = url
    self.request.method = method
    self.request.save()

    print(f'saving {method} {url} to request {self.request.id}')

  def form_field_changed(self, field, value):
    original_value = getattr(self.request, field)
    # TODO: Check if the item is modified and update self.modified

  def hide_fuzz_table(self):
    self.ui.fuzzRequestsTable.setVisible(False)
    self.ui.toggleFuzzTableButton.setText(">>")

  @Slot()
  def toggle_fuzz_table(self):
    visible = not self.ui.fuzzRequestsTable.isVisible()
    self.ui.fuzzRequestsTable.setVisible(visible)

    if visible:
      self.restore_layout_state()

    if (visible):
      self.ui.toggleFuzzTableButton.setText("<<")
    else:
      self.ui.toggleFuzzTableButton.setText(">>")

  def restore_layout_state(self):
    splitter_state = self.settings.get("RequestEditPage.splitter", None)
    splitter_state2 = self.settings.get("RequestEditPage.splitter2", None)

    self.ui.splitter.restoreState(splitter_state)
    self.ui.splitter2.restoreState(splitter_state2)

  def save_layout_state(self):
    splitter_state = self.ui.splitter.saveState()
    splitter_state2 = self.ui.splitter2.saveState()

    self.settings.save("RequestEditPage.splitter", splitter_state)
    self.settings.save("RequestEditPage.splitter2", splitter_state2)

  def set_method_on_form(self, method):
    if method == None:
      index = 0
    else:
      index = self.METHODS.index(method)

    self.ui.methodInput.setCurrentIndex(index)

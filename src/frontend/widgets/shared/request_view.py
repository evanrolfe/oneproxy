import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtWebEngineWidgets import QWebEngineView

from ui_compiled.shared.ui_request_view import Ui_RequestView

from widgets.code_editor.html_highlighter import HtmlHighlighter

TABS_STYLE = """
  QTabWidget::pane {
    margin: 1px 1px 1px 1px;
    padding: -1px;
  }
"""

class RequestView(QWidget):
  def __init__(self, *args, **kwargs):
    super(RequestView, self).__init__(*args, **kwargs)
    self.ui = Ui_RequestView()
    self.ui.setupUi(self)

    self.ui.headerTabs.setStyleSheet(TABS_STYLE)
    self.ui.bodyTabs.setStyleSheet(TABS_STYLE)

    # Disable modified tabs to start with:
    self.ui.headerTabs.setTabEnabled(1, False)
    self.ui.headerTabs.setTabEnabled(3, False)

    #self.highlighter = HtmlHighlighter(self.ui.responseBodyRawText.document())
    #self.ui.bodyTab.setCurrentWidget(self.ui.responseBodyWebview)

  def set_request(self, request):
    self.ui.requestHeadersText.setPlainText(request.request_headers_parsed())
    self.ui.responseHeadersText.setPlainText(request.response_headers_parsed())

    self.ui.responseBodyRawText.setPlainText(request.response_body)
    self.ui.responseBodyModifiedText.setPlainText(request.modified_response_body)
    self.ui.responseBodyParsedText.setPlainText(request.response_body_rendered)
    self.ui.responseBodyPreview.setHtml(request.response_body_rendered)

    # Request modified tab:
    if (request.request_modified == True):
      self.ui.headerTabs.setTabEnabled(1, True)
      self.ui.requestHeadersModifiedText.setPlainText(request.request_headers_modified_parsed())
    else:
      self.ui.headerTabs.setTabEnabled(1, False)

    # Response modified tab:
    if (request.response_modified == True):
      self.ui.headerTabs.setTabEnabled(3, True)
      self.ui.bodyTabs.setTabEnabled(1, True)
      self.ui.responseHeadersModifiedText.setPlainText(request.response_headers_modified_parsed())
    else:
      self.ui.headerTabs.setTabEnabled(3, False)
      self.ui.bodyTabs.setTabEnabled(1, False)

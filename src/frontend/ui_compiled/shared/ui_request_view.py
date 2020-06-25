# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_view.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView


class Ui_RequestView(object):
    def setupUi(self, RequestView):
        if not RequestView.objectName():
            RequestView.setObjectName(u"RequestView")
        RequestView.resize(590, 678)
        self.verticalLayout_2 = QVBoxLayout(RequestView)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(RequestView)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.headerTabs = QTabWidget(self.splitter)
        self.headerTabs.setObjectName(u"headerTabs")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerTabs.sizePolicy().hasHeightForWidth())
        self.headerTabs.setSizePolicy(sizePolicy)
        self.requestTab = QWidget()
        self.requestTab.setObjectName(u"requestTab")
        self.verticalLayout_4 = QVBoxLayout(self.requestTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.requestHeadersText = QPlainTextEdit(self.requestTab)
        self.requestHeadersText.setObjectName(u"requestHeadersText")

        self.verticalLayout_4.addWidget(self.requestHeadersText)

        self.headerTabs.addTab(self.requestTab, "")
        self.requestModifiedTab = QWidget()
        self.requestModifiedTab.setObjectName(u"requestModifiedTab")
        self.requestModifiedTab.setEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(self.requestModifiedTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.requestHeadersModifiedText = QPlainTextEdit(self.requestModifiedTab)
        self.requestHeadersModifiedText.setObjectName(u"requestHeadersModifiedText")

        self.verticalLayout_3.addWidget(self.requestHeadersModifiedText)

        self.headerTabs.addTab(self.requestModifiedTab, "")
        self.responseTab = QWidget()
        self.responseTab.setObjectName(u"responseTab")
        self.verticalLayout = QVBoxLayout(self.responseTab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.responseHeadersText = QPlainTextEdit(self.responseTab)
        self.responseHeadersText.setObjectName(u"responseHeadersText")

        self.verticalLayout.addWidget(self.responseHeadersText)

        self.headerTabs.addTab(self.responseTab, "")
        self.responseModifiedTab = QWidget()
        self.responseModifiedTab.setObjectName(u"responseModifiedTab")
        self.responseModifiedTab.setEnabled(True)
        self.verticalLayout_5 = QVBoxLayout(self.responseModifiedTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.responseHeadersModifiedText = QPlainTextEdit(self.responseModifiedTab)
        self.responseHeadersModifiedText.setObjectName(u"responseHeadersModifiedText")

        self.verticalLayout_5.addWidget(self.responseHeadersModifiedText)

        self.headerTabs.addTab(self.responseModifiedTab, "")
        self.splitter.addWidget(self.headerTabs)
        self.bodyTabs = QTabWidget(self.splitter)
        self.bodyTabs.setObjectName(u"bodyTabs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.bodyTabs.sizePolicy().hasHeightForWidth())
        self.bodyTabs.setSizePolicy(sizePolicy1)
        self.responseBodyText = QPlainTextEdit()
        self.responseBodyText.setObjectName(u"responseBodyText")
        self.bodyTabs.addTab(self.responseBodyText, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.bodyTabs.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.bodyTabs.addTab(self.tab, "")
        self.responseBodyWebview = QWebEngineView()
        self.responseBodyWebview.setObjectName(u"responseBodyWebview")
        self.bodyTabs.addTab(self.responseBodyWebview, "")
        self.splitter.addWidget(self.bodyTabs)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(RequestView)

        self.headerTabs.setCurrentIndex(3)
        self.bodyTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RequestView)
    # setupUi

    def retranslateUi(self, RequestView):
        RequestView.setWindowTitle(QCoreApplication.translate("RequestView", u"Form", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.requestTab), QCoreApplication.translate("RequestView", u"Request", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.requestModifiedTab), QCoreApplication.translate("RequestView", u"(Modified)", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.responseTab), QCoreApplication.translate("RequestView", u"Response", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.responseModifiedTab), QCoreApplication.translate("RequestView", u"(Modified)", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyText), QCoreApplication.translate("RequestView", u"Raw", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.tab_2), QCoreApplication.translate("RequestView", u"(Modified)", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.tab), QCoreApplication.translate("RequestView", u"Parsed", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyWebview), QCoreApplication.translate("RequestView", u"Preview", None))
    # retranslateUi


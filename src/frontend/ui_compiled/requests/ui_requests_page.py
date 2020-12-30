# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'requests_page.ui'
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


class Ui_RequestsPage(object):
    def setupUi(self, RequestsPage):
        if not RequestsPage.objectName():
            RequestsPage.setObjectName(u"RequestsPage")
        RequestsPage.resize(897, 581)
        self.verticalLayout_2 = QVBoxLayout(RequestsPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(RequestsPage)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.splitter_2 = QSplitter(RequestsPage)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.requestsTreeView = QTreeView(self.splitter_2)
        self.requestsTreeView.setObjectName(u"requestsTreeView")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestsTreeView.sizePolicy().hasHeightForWidth())
        self.requestsTreeView.setSizePolicy(sizePolicy)
        self.splitter_2.addWidget(self.requestsTreeView)
        self.fuzzRequestsTable = QTableView(self.splitter_2)
        self.fuzzRequestsTable.setObjectName(u"fuzzRequestsTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fuzzRequestsTable.sizePolicy().hasHeightForWidth())
        self.fuzzRequestsTable.setSizePolicy(sizePolicy1)
        self.splitter_2.addWidget(self.fuzzRequestsTable)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy2)
        self.splitter.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.requestActionsLayout = QHBoxLayout()
        self.requestActionsLayout.setObjectName(u"requestActionsLayout")
        self.requestActionsLayout.setContentsMargins(0, 5, 5, -1)
        self.toggleFuzzTableButton = QPushButton(self.layoutWidget)
        self.toggleFuzzTableButton.setObjectName(u"toggleFuzzTableButton")
        self.toggleFuzzTableButton.setMaximumSize(QSize(35, 16777215))

        self.requestActionsLayout.addWidget(self.toggleFuzzTableButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.requestActionsLayout.addItem(self.horizontalSpacer)

        self.sendRequestButton = QPushButton(self.layoutWidget)
        self.sendRequestButton.setObjectName(u"sendRequestButton")

        self.requestActionsLayout.addWidget(self.sendRequestButton)

        self.saveRequestButton = QPushButton(self.layoutWidget)
        self.saveRequestButton.setObjectName(u"saveRequestButton")

        self.requestActionsLayout.addWidget(self.saveRequestButton)


        self.verticalLayout.addLayout(self.requestActionsLayout)

        self.requestTabs = QTabWidget(self.layoutWidget)
        self.requestTabs.setObjectName(u"requestTabs")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.requestTabs.sizePolicy().hasHeightForWidth())
        self.requestTabs.setSizePolicy(sizePolicy3)
        self.requestTab = QWidget()
        self.requestTab.setObjectName(u"requestTab")
        self.verticalLayout_4 = QVBoxLayout(self.requestTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.requestText = QPlainTextEdit(self.requestTab)
        self.requestText.setObjectName(u"requestText")

        self.verticalLayout_4.addWidget(self.requestText)

        self.requestTabs.addTab(self.requestTab, "")

        self.verticalLayout.addWidget(self.requestTabs)

        self.splitter.addWidget(self.layoutWidget)
        self.responseTabs = QTabWidget(self.splitter)
        self.responseTabs.setObjectName(u"responseTabs")
        sizePolicy3.setHeightForWidth(self.responseTabs.sizePolicy().hasHeightForWidth())
        self.responseTabs.setSizePolicy(sizePolicy3)
        self.responseTab = QWidget()
        self.responseTab.setObjectName(u"responseTab")
        self.verticalLayout_4_body = QVBoxLayout(self.responseTab)
        self.verticalLayout_4_body.setObjectName(u"verticalLayout_4_body")
        self.verticalLayout_4_body.setContentsMargins(0, 0, 0, 0)
        self.responseText = QPlainTextEdit(self.responseTab)
        self.responseText.setObjectName(u"responseText")

        self.verticalLayout_4_body.addWidget(self.responseText)

        self.responseTabs.addTab(self.responseTab, "")
        self.responseBodyTab = QWidget()
        self.responseBodyTab.setObjectName(u"responseBodyTab")
        self.responseBodyTab.setEnabled(True)
        self.responseBodyText = QPlainTextEdit(self.responseBodyTab)
        self.responseBodyText.setObjectName(u"responseBodyText")
        self.responseBodyText.setGeometry(QRect(0, 0, 256, 192))
        self.responseTabs.addTab(self.responseBodyTab, "")
        self.splitter.addWidget(self.responseTabs)
        self.splitter_2.addWidget(self.splitter)

        self.verticalLayout_2.addWidget(self.splitter_2)


        self.retranslateUi(RequestsPage)

        self.requestTabs.setCurrentIndex(0)
        self.responseTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RequestsPage)
    # setupUi

    def retranslateUi(self, RequestsPage):
        RequestsPage.setWindowTitle(QCoreApplication.translate("RequestsPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("RequestsPage", u"EDITOR", None))
        self.toggleFuzzTableButton.setText(QCoreApplication.translate("RequestsPage", u"<<", None))
        self.sendRequestButton.setText(QCoreApplication.translate("RequestsPage", u"Send", None))
        self.saveRequestButton.setText(QCoreApplication.translate("RequestsPage", u"Save", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestTab), QCoreApplication.translate("RequestsPage", u"Request", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseTab), QCoreApplication.translate("RequestsPage", u"Response", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyTab), QCoreApplication.translate("RequestsPage", u"Body", None))
    # retranslateUi


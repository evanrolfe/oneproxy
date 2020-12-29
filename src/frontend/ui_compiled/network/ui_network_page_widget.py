# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_page_widget.ui'
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

from widgets.network.network_requests_table import NetworkRequestsTable
from widgets.shared.request_view import RequestView


class Ui_NetworkPageWidget(object):
    def setupUi(self, NetworkPageWidget):
        if not NetworkPageWidget.objectName():
            NetworkPageWidget.setObjectName(u"NetworkPageWidget")
        NetworkPageWidget.resize(1200, 800)
        self.horizontalLayout = QHBoxLayout(NetworkPageWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.requestsTableAndViewSplitter = QSplitter(NetworkPageWidget)
        self.requestsTableAndViewSplitter.setObjectName(u"requestsTableAndViewSplitter")
        self.requestsTableAndViewSplitter.setOrientation(Qt.Horizontal)
        self.requestsTableWidget = NetworkRequestsTable(self.requestsTableAndViewSplitter)
        self.requestsTableWidget.setObjectName(u"requestsTableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestsTableWidget.sizePolicy().hasHeightForWidth())
        self.requestsTableWidget.setSizePolicy(sizePolicy)
        self.requestsTableWidget.setMinimumSize(QSize(740, 0))
        self.requestsTableAndViewSplitter.addWidget(self.requestsTableWidget)
        self.requestViewWidget = RequestView(self.requestsTableAndViewSplitter)
        self.requestViewWidget.setObjectName(u"requestViewWidget")
        sizePolicy.setHeightForWidth(self.requestViewWidget.sizePolicy().hasHeightForWidth())
        self.requestViewWidget.setSizePolicy(sizePolicy)
        self.requestsTableAndViewSplitter.addWidget(self.requestViewWidget)

        self.horizontalLayout.addWidget(self.requestsTableAndViewSplitter)


        self.retranslateUi(NetworkPageWidget)

        QMetaObject.connectSlotsByName(NetworkPageWidget)
    # setupUi

    def retranslateUi(self, NetworkPageWidget):
        NetworkPageWidget.setWindowTitle(QCoreApplication.translate("NetworkPageWidget", u"Form", None))
    # retranslateUi


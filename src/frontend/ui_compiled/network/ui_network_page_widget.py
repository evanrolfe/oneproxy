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
        self.splitter = QSplitter(NetworkPageWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.requestsTableWidget = NetworkRequestsTable(self.splitter)
        self.requestsTableWidget.setObjectName(u"requestsTableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestsTableWidget.sizePolicy().hasHeightForWidth())
        self.requestsTableWidget.setSizePolicy(sizePolicy)
        self.requestsTableWidget.setMinimumSize(QSize(740, 0))
        self.splitter.addWidget(self.requestsTableWidget)
        self.requestViewWidget = RequestView(self.splitter)
        self.requestViewWidget.setObjectName(u"requestViewWidget")
        sizePolicy.setHeightForWidth(self.requestViewWidget.sizePolicy().hasHeightForWidth())
        self.requestViewWidget.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.requestViewWidget)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(NetworkPageWidget)

        QMetaObject.connectSlotsByName(NetworkPageWidget)
    # setupUi

    def retranslateUi(self, NetworkPageWidget):
        NetworkPageWidget.setWindowTitle(QCoreApplication.translate("NetworkPageWidget", u"Form", None))
    # retranslateUi


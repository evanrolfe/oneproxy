# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_requests_table.ui'
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


class Ui_NetworkRequestsTable(object):
    def setupUi(self, NetworkRequestsTable):
        if not NetworkRequestsTable.objectName():
            NetworkRequestsTable.setObjectName(u"NetworkRequestsTable")
        NetworkRequestsTable.resize(424, 702)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NetworkRequestsTable.sizePolicy().hasHeightForWidth())
        NetworkRequestsTable.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(NetworkRequestsTable)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.requestsTable = QTableView(NetworkRequestsTable)
        self.requestsTable.setObjectName(u"requestsTable")

        self.horizontalLayout.addWidget(self.requestsTable)


        self.retranslateUi(NetworkRequestsTable)

        QMetaObject.connectSlotsByName(NetworkRequestsTable)
    # setupUi

    def retranslateUi(self, NetworkRequestsTable):
        NetworkRequestsTable.setWindowTitle(QCoreApplication.translate("NetworkRequestsTable", u"Form", None))
    # retranslateUi


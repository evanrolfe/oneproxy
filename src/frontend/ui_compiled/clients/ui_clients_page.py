# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clients_page.ui'
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

from widgets.clients.clients_table import ClientsTable
from widgets.clients.client_view import ClientView


class Ui_ClientsPage(object):
    def setupUi(self, NetworkWidget):
        if not NetworkWidget.objectName():
            NetworkWidget.setObjectName(u"NetworkWidget")
        NetworkWidget.resize(897, 581)
        self.horizontalLayout = QHBoxLayout(NetworkWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(NetworkWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.clientsTable = ClientsTable(self.splitter)
        self.clientsTable.setObjectName(u"clientsTable")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clientsTable.sizePolicy().hasHeightForWidth())
        self.clientsTable.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.clientsTable)
        self.clientView = ClientView(self.splitter)
        self.clientView.setObjectName(u"clientView")
        sizePolicy.setHeightForWidth(self.clientView.sizePolicy().hasHeightForWidth())
        self.clientView.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.clientView)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(NetworkWidget)

        QMetaObject.connectSlotsByName(NetworkWidget)
    # setupUi

    def retranslateUi(self, NetworkWidget):
        NetworkWidget.setWindowTitle(QCoreApplication.translate("ClientsPage", u"Form", None))
    # retranslateUi


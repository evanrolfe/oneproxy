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
        NetworkRequestsTable.resize(509, 702)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NetworkRequestsTable.sizePolicy().hasHeightForWidth())
        NetworkRequestsTable.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(NetworkRequestsTable)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(NetworkRequestsTable)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(NetworkRequestsTable)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_2.addWidget(self.lineEdit)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(NetworkRequestsTable)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.displayFiltersButton = QPushButton(NetworkRequestsTable)
        self.displayFiltersButton.setObjectName(u"displayFiltersButton")

        self.horizontalLayout.addWidget(self.displayFiltersButton)

        self.captureFiltersButton = QPushButton(NetworkRequestsTable)
        self.captureFiltersButton.setObjectName(u"captureFiltersButton")

        self.horizontalLayout.addWidget(self.captureFiltersButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.requestsTable = QTableView(NetworkRequestsTable)
        self.requestsTable.setObjectName(u"requestsTable")

        self.verticalLayout_3.addWidget(self.requestsTable)


        self.retranslateUi(NetworkRequestsTable)

        QMetaObject.connectSlotsByName(NetworkRequestsTable)
    # setupUi

    def retranslateUi(self, NetworkRequestsTable):
        NetworkRequestsTable.setWindowTitle(QCoreApplication.translate("NetworkRequestsTable", u"Form", None))
        self.label.setText(QCoreApplication.translate("NetworkRequestsTable", u"Search:", None))
        self.label_2.setText(QCoreApplication.translate("NetworkRequestsTable", u"Filters:", None))
        self.displayFiltersButton.setText(QCoreApplication.translate("NetworkRequestsTable", u"Display", None))
        self.captureFiltersButton.setText(QCoreApplication.translate("NetworkRequestsTable", u"Capture", None))
    # retranslateUi


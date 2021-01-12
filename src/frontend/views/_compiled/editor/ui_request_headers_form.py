# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_headers_form.ui'
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


class Ui_RequestHeadersForm(object):
    def setupUi(self, requestHeadersForm):
        if not requestHeadersForm.objectName():
            requestHeadersForm.setObjectName(u"requestHeadersForm")
        requestHeadersForm.resize(880, 521)
        self.verticalLayout_2 = QVBoxLayout(requestHeadersForm)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.headersLayout = QVBoxLayout()
        self.headersLayout.setObjectName(u"headersLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.showGeneratedHeaders = QCheckBox(requestHeadersForm)
        self.showGeneratedHeaders.setObjectName(u"showGeneratedHeaders")
        self.showGeneratedHeaders.setChecked(True)

        self.horizontalLayout.addWidget(self.showGeneratedHeaders)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.headersLayout.addLayout(self.horizontalLayout)

        self.headersTable = QTableView(requestHeadersForm)
        self.headersTable.setObjectName(u"headersTable")

        self.headersLayout.addWidget(self.headersTable)


        self.verticalLayout_2.addLayout(self.headersLayout)


        self.retranslateUi(requestHeadersForm)

        QMetaObject.connectSlotsByName(requestHeadersForm)
    # setupUi

    def retranslateUi(self, requestHeadersForm):
        self.showGeneratedHeaders.setText(QCoreApplication.translate("RequestHeadersForm", u"Include auto-generated headers", None))
        pass
    # retranslateUi


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
    def setupUi(self, form):
        if not form.objectName():
            form.setObjectName(u"form")
        form.resize(880, 521)
        self.horizontalLayout = QHBoxLayout(form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.showGeneratedHeaders = QCheckBox(form)
        self.showGeneratedHeaders.setObjectName(u"showGeneratedHeaders")
        self.showGeneratedHeaders.setChecked(True)

        self.verticalLayout.addWidget(self.showGeneratedHeaders)

        self.headersTable = QTableView(form)
        self.headersTable.setObjectName(u"headersTable")

        self.verticalLayout.addWidget(self.headersTable)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(form)

        QMetaObject.connectSlotsByName(form)
    # setupUi

    def retranslateUi(self, form):
        self.showGeneratedHeaders.setText(QCoreApplication.translate("RequestHeadersForm", u"Include auto-generated headers", None))
        pass
    # retranslateUi


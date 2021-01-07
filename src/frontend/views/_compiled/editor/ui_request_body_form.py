# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_body_form.ui'
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


class Ui_RequestBodyForm(object):
    def setupUi(self, form):
        if not form.objectName():
            form.setObjectName(u"form")
        form.resize(880, 521)
        self.verticalLayout = QVBoxLayout(form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton = QRadioButton(form)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(form)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(form)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout.addWidget(self.radioButton_3)

        self.radioButton_4 = QRadioButton(form)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.horizontalLayout.addWidget(self.radioButton_4)

        self.horizontalSpacer = QSpacerItem(148, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.requestBodyInput = QPlainTextEdit(form)
        self.requestBodyInput.setObjectName(u"requestBodyInput")

        self.verticalLayout.addWidget(self.requestBodyInput)


        self.retranslateUi(form)

        QMetaObject.connectSlotsByName(form)
    # setupUi

    def retranslateUi(self, form):
        self.radioButton.setText(QCoreApplication.translate("RequestBodyForm", u"form-data", None))
        self.radioButton_2.setText(QCoreApplication.translate("RequestBodyForm", u"x-www-form-urlencoded", None))
        self.radioButton_3.setText(QCoreApplication.translate("RequestBodyForm", u"raw", None))
        self.radioButton_4.setText(QCoreApplication.translate("RequestBodyForm", u"binary", None))
        pass
    # retranslateUi


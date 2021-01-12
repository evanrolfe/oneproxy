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
    def setupUi(self, RequestBodyForm):
        if not RequestBodyForm.objectName():
            RequestBodyForm.setObjectName(u"RequestBodyForm")
        RequestBodyForm.resize(880, 521)
        self.requestBodyFormLayout = QVBoxLayout(RequestBodyForm)
        self.requestBodyFormLayout.setObjectName(u"requestBodyFormLayout")
        self.requestBodyFormLayout.setContentsMargins(0, 0, 0, 0)
        self.requestBodyFormHLayout = QHBoxLayout()
        self.requestBodyFormHLayout.setObjectName(u"requestBodyFormHLayout")
        self.requestBodyFormHLayout.setContentsMargins(10, 5, 10, 5)
        self.radioButton = QRadioButton(RequestBodyForm)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setCheckable(False)

        self.requestBodyFormHLayout.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(RequestBodyForm)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setCheckable(False)

        self.requestBodyFormHLayout.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(RequestBodyForm)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setCheckable(True)
        self.radioButton_3.setChecked(True)

        self.requestBodyFormHLayout.addWidget(self.radioButton_3)

        self.radioButton_4 = QRadioButton(RequestBodyForm)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setCheckable(False)

        self.requestBodyFormHLayout.addWidget(self.radioButton_4)

        self.horizontalSpacer = QSpacerItem(148, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.requestBodyFormHLayout.addItem(self.horizontalSpacer)


        self.requestBodyFormLayout.addLayout(self.requestBodyFormHLayout)

        self.requestBodyInput = QPlainTextEdit(RequestBodyForm)
        self.requestBodyInput.setObjectName(u"requestBodyInput")

        self.requestBodyFormLayout.addWidget(self.requestBodyInput)


        self.retranslateUi(RequestBodyForm)

        QMetaObject.connectSlotsByName(RequestBodyForm)
    # setupUi

    def retranslateUi(self, RequestBodyForm):
        self.radioButton.setText(QCoreApplication.translate("RequestBodyForm", u"form-data", None))
        self.radioButton_2.setText(QCoreApplication.translate("RequestBodyForm", u"x-www-form-urlencoded", None))
        self.radioButton_3.setText(QCoreApplication.translate("RequestBodyForm", u"raw", None))
        self.radioButton_4.setText(QCoreApplication.translate("RequestBodyForm", u"binary", None))
        pass
    # retranslateUi


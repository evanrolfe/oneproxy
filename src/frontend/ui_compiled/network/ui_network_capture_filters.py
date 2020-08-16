# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_capture_filters.ui'
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


class Ui_NetworkCaptureFilters(object):
    def setupUi(self, NetworkCaptureFilters):
        if not NetworkCaptureFilters.objectName():
            NetworkCaptureFilters.setObjectName(u"NetworkCaptureFilters")
        NetworkCaptureFilters.resize(700, 300)
        self.verticalLayout_2 = QVBoxLayout(NetworkCaptureFilters)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.descLabel = QLabel(NetworkCaptureFilters)
        self.descLabel.setObjectName(u"descLabel")

        self.verticalLayout.addWidget(self.descLabel)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(NetworkCaptureFilters)

        QMetaObject.connectSlotsByName(NetworkCaptureFilters)
    # setupUi

    def retranslateUi(self, NetworkCaptureFilters):
        NetworkCaptureFilters.setWindowTitle(QCoreApplication.translate("NetworkCaptureFilters", u"New Client", None))
        self.descLabel.setText(QCoreApplication.translate("NetworkCaptureFilters", u"Capture FILTERS GO HERE!", None))
    # retranslateUi


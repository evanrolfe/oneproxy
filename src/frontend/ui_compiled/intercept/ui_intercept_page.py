# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'intercept_page.ui'
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


class Ui_InterceptPage(object):
    def setupUi(self, InterceptPage):
        if not InterceptPage.objectName():
            InterceptPage.setObjectName(u"InterceptPage")
        InterceptPage.resize(741, 511)
        self.horizontalLayout_2 = QHBoxLayout(InterceptPage)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.interceptTitle = QLabel(InterceptPage)
        self.interceptTitle.setObjectName(u"interceptTitle")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.interceptTitle.setFont(font)

        self.verticalLayout_2.addWidget(self.interceptTitle)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.forwardButton = QPushButton(InterceptPage)
        self.forwardButton.setObjectName(u"forwardButton")

        self.horizontalLayout.addWidget(self.forwardButton)

        self.forwardInterceptButton = QPushButton(InterceptPage)
        self.forwardInterceptButton.setObjectName(u"forwardInterceptButton")

        self.horizontalLayout.addWidget(self.forwardInterceptButton)

        self.dropButton = QPushButton(InterceptPage)
        self.dropButton.setObjectName(u"dropButton")

        self.horizontalLayout.addWidget(self.dropButton)

        self.enabledButton = QPushButton(InterceptPage)
        self.enabledButton.setObjectName(u"enabledButton")

        self.horizontalLayout.addWidget(self.enabledButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.interceptTabs = QTabWidget(InterceptPage)
        self.interceptTabs.setObjectName(u"interceptTabs")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interceptTabs.sizePolicy().hasHeightForWidth())
        self.interceptTabs.setSizePolicy(sizePolicy)
        self.headersTab = QWidget()
        self.headersTab.setObjectName(u"headersTab")
        self.verticalLayout_4 = QVBoxLayout(self.headersTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.headersText = QPlainTextEdit(self.headersTab)
        self.headersText.setObjectName(u"headersText")

        self.verticalLayout_4.addWidget(self.headersText)

        self.interceptTabs.addTab(self.headersTab, "")
        self.bodyTab = QWidget()
        self.bodyTab.setObjectName(u"bodyTab")
        self.verticalLayout = QVBoxLayout(self.bodyTab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.bodyText = QPlainTextEdit(self.bodyTab)
        self.bodyText.setObjectName(u"bodyText")

        self.verticalLayout.addWidget(self.bodyText)

        self.interceptTabs.addTab(self.bodyTab, "")

        self.verticalLayout_3.addWidget(self.interceptTabs)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.retranslateUi(InterceptPage)

        self.interceptTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(InterceptPage)
    # setupUi

    def retranslateUi(self, InterceptPage):
        InterceptPage.setWindowTitle(QCoreApplication.translate("InterceptPage", u"Form", None))
        self.interceptTitle.setText(QCoreApplication.translate("InterceptPage", u"Intercepted Request:", None))
        self.forwardButton.setText(QCoreApplication.translate("InterceptPage", u"Forward", None))
        self.forwardInterceptButton.setText(QCoreApplication.translate("InterceptPage", u"Forward + Intercept Response", None))
        self.dropButton.setText(QCoreApplication.translate("InterceptPage", u"Drop", None))
        self.enabledButton.setText(QCoreApplication.translate("InterceptPage", u"Enable Intercept", None))
        self.interceptTabs.setTabText(self.interceptTabs.indexOf(self.headersTab), QCoreApplication.translate("InterceptPage", u"Headers", None))
        self.interceptTabs.setTabText(self.interceptTabs.indexOf(self.bodyTab), QCoreApplication.translate("InterceptPage", u"Body", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor_page.ui'
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

from widgets.editor.tabs import Tabs
from widgets.editor.item_explorer import ItemExplorer


class Ui_EditorPage(object):
    def setupUi(self, EditorPage):
        if not EditorPage.objectName():
            EditorPage.setObjectName(u"EditorPage")
        EditorPage.resize(897, 581)
        self.verticalLayout = QVBoxLayout(EditorPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(EditorPage)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.splitter = QSplitter(EditorPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.itemExplorer = ItemExplorer(self.splitter)
        self.itemExplorer.setObjectName(u"itemExplorer")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemExplorer.sizePolicy().hasHeightForWidth())
        self.itemExplorer.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.itemExplorer)
        self.tabs = Tabs(self.splitter)
        self.tabs.setObjectName(u"tabs")
        self.splitter.addWidget(self.tabs)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(EditorPage)

        QMetaObject.connectSlotsByName(EditorPage)
    # setupUi

    def retranslateUi(self, EditorPage):
        EditorPage.setWindowTitle(QCoreApplication.translate("EditorPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("EditorPage", u"EDITOR", None))
    # retranslateUi


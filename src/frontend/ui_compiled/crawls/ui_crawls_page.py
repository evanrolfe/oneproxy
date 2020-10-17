# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crawls_page.ui'
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

from widgets.crawls.crawls_table import CrawlsTable
from widgets.crawls.crawl_view import CrawlView


class Ui_CrawlsPage(object):
    def setupUi(self, CrawlsPage):
        if not CrawlsPage.objectName():
            CrawlsPage.setObjectName(u"CrawlsPage")
        CrawlsPage.resize(897, 581)
        self.verticalLayout_2 = QVBoxLayout(CrawlsPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(CrawlsPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.crawlerToolbar = QWidget(self.layoutWidget)
        self.crawlerToolbar.setObjectName(u"crawlerToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crawlerToolbar.sizePolicy().hasHeightForWidth())
        self.crawlerToolbar.setSizePolicy(sizePolicy)
        self.crawlerToolbar.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.crawlerToolbar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.crawlerToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.newCrawlerButton = QPushButton(self.crawlerToolbar)
        self.newCrawlerButton.setObjectName(u"newCrawlerButton")

        self.horizontalLayout.addWidget(self.newCrawlerButton)


        self.verticalLayout.addWidget(self.crawlerToolbar)

        self.crawlsTable = CrawlsTable(self.layoutWidget)
        self.crawlsTable.setObjectName(u"crawlsTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.crawlsTable.sizePolicy().hasHeightForWidth())
        self.crawlsTable.setSizePolicy(sizePolicy1)
        self.crawlsTable.setMinimumSize(QSize(350, 0))

        self.verticalLayout.addWidget(self.crawlsTable)

        self.splitter.addWidget(self.layoutWidget)
        self.crawlView = CrawlView(self.splitter)
        self.crawlView.setObjectName(u"crawlView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.crawlView.sizePolicy().hasHeightForWidth())
        self.crawlView.setSizePolicy(sizePolicy2)
        self.splitter.addWidget(self.crawlView)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(CrawlsPage)

        QMetaObject.connectSlotsByName(CrawlsPage)
    # setupUi

    def retranslateUi(self, CrawlsPage):
        CrawlsPage.setWindowTitle(QCoreApplication.translate("CrawlsPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("CrawlsPage", u"Crawler History:", None))
        self.newCrawlerButton.setText(QCoreApplication.translate("CrawlsPage", u"New Crawler", None))
    # retranslateUi


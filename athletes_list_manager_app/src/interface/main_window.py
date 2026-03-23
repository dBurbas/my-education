# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(957, 600)
        MainWindow.setMinimumSize(QSize(900, 600))
        MainWindow.setBaseSize(QSize(1100, 700))
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_4 = QAction(MainWindow)
        self.action_4.setObjectName(u"action_4")
        self.action_5 = QAction(MainWindow)
        self.action_5.setObjectName(u"action_5")
        self.action_6 = QAction(MainWindow)
        self.action_6.setObjectName(u"action_6")
        self.action_7 = QAction(MainWindow)
        self.action_7.setObjectName(u"action_7")
        self.action_8 = QAction(MainWindow)
        self.action_8.setObjectName(u"action_8")
        self.action_10 = QAction(MainWindow)
        self.action_10.setObjectName(u"action_10")
        self.action_11 = QAction(MainWindow)
        self.action_11.setObjectName(u"action_11")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"font-size:14pt;")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(225, 0))
        self.sidebar.setMaximumSize(QSize(250, 16777215))
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.sidebar)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_head = QFrame(self.sidebar)
        self.sidebar_head.setObjectName(u"sidebar_head")
        self.sidebar_head.setMinimumSize(QSize(0, 75))
        self.sidebar_head.setMaximumSize(QSize(16777215, 75))
        self.sidebar_head.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar_head.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.sidebar_head)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(15, 0, 15, 0)
        self.app_logo = QGraphicsView(self.sidebar_head)
        self.app_logo.setObjectName(u"app_logo")
        self.app_logo.setMinimumSize(QSize(0, 0))
        self.app_logo.setMaximumSize(QSize(60, 60))

        self.horizontalLayout_2.addWidget(self.app_logo)

        self.app_label = QLabel(self.sidebar_head)
        self.app_label.setObjectName(u"app_label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.app_label.setFont(font)

        self.horizontalLayout_2.addWidget(self.app_label)


        self.verticalLayout.addWidget(self.sidebar_head)

        self.sidebar_buttons = QFrame(self.sidebar)
        self.sidebar_buttons.setObjectName(u"sidebar_buttons")
        self.sidebar_buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.sidebar_buttons)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(15, 15, 15, 15)
        self.add_button = QPushButton(self.sidebar_buttons)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setMinimumSize(QSize(0, 60))

        self.verticalLayout_4.addWidget(self.add_button)

        self.delete_button = QPushButton(self.sidebar_buttons)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setMinimumSize(QSize(0, 60))

        self.verticalLayout_4.addWidget(self.delete_button)

        self.search_button = QPushButton(self.sidebar_buttons)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setMinimumSize(QSize(0, 60))

        self.verticalLayout_4.addWidget(self.search_button)

        self.buttons_spacer = QSpacerItem(20, 176, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.buttons_spacer)

        self.settings_button = QPushButton(self.sidebar_buttons)
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setMinimumSize(QSize(0, 60))

        self.verticalLayout_4.addWidget(self.settings_button)


        self.verticalLayout.addWidget(self.sidebar_buttons)


        self.horizontalLayout.addWidget(self.sidebar)

        self.main_part = QFrame(self.centralwidget)
        self.main_part.setObjectName(u"main_part")
        self.main_part.setMinimumSize(QSize(650, 0))
        self.main_part.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_part.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.main_part)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.table_head = QFrame(self.main_part)
        self.table_head.setObjectName(u"table_head")
        self.table_head.setMinimumSize(QSize(0, 75))
        self.table_head.setMaximumSize(QSize(16777215, 75))
        self.table_head.setFrameShape(QFrame.Shape.StyledPanel)
        self.table_head.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.table_head)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 5, 10, 5)
        self.table_name_label = QLabel(self.table_head)
        self.table_name_label.setObjectName(u"table_name_label")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(False)
        self.table_name_label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.table_name_label)

        self.table_head_spacer = QSpacerItem(128, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.table_head_spacer)

        self.table_head_divide = QFrame(self.table_head)
        self.table_head_divide.setObjectName(u"table_head_divide")
        self.table_head_divide.setFrameShape(QFrame.Shape.VLine)
        self.table_head_divide.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.table_head_divide)

        self.file_name_label = QLabel(self.table_head)
        self.file_name_label.setObjectName(u"file_name_label")
        font2 = QFont()
        font2.setPointSize(14)
        self.file_name_label.setFont(font2)

        self.horizontalLayout_3.addWidget(self.file_name_label)

        self.save_button = QPushButton(self.table_head)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setMinimumSize(QSize(0, 60))
        self.save_button.setFont(font2)

        self.horizontalLayout_3.addWidget(self.save_button)

        self.load_button = QPushButton(self.table_head)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setMinimumSize(QSize(0, 60))
        self.load_button.setFont(font2)

        self.horizontalLayout_3.addWidget(self.load_button)


        self.verticalLayout_2.addWidget(self.table_head)

        self.table_part = QFrame(self.main_part)
        self.table_part.setObjectName(u"table_part")
        self.table_part.setFrameShape(QFrame.Shape.StyledPanel)
        self.table_part.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.table_part)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tableView = QTableView(self.table_part)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_3.addWidget(self.tableView)

        self.pagination = QFrame(self.table_part)
        self.pagination.setObjectName(u"pagination")
        self.pagination.setMinimumSize(QSize(500, 50))
        self.pagination.setMaximumSize(QSize(16777215, 50))
        self.pagination.setFrameShape(QFrame.Shape.StyledPanel)
        self.pagination.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.pagination)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.pagination)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(16777215, 45))

        self.horizontalLayout_4.addWidget(self.label)

        self.pagination_spacer = QSpacerItem(193, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.pagination_spacer)

        self.prev_pagination_button = QPushButton(self.pagination)
        self.prev_pagination_button.setObjectName(u"prev_pagination_button")
        sizePolicy.setHeightForWidth(self.prev_pagination_button.sizePolicy().hasHeightForWidth())
        self.prev_pagination_button.setSizePolicy(sizePolicy)
        self.prev_pagination_button.setMinimumSize(QSize(0, 45))

        self.horizontalLayout_4.addWidget(self.prev_pagination_button)

        self.first_page_button = QPushButton(self.pagination)
        self.first_page_button.setObjectName(u"first_page_button")
        sizePolicy.setHeightForWidth(self.first_page_button.sizePolicy().hasHeightForWidth())
        self.first_page_button.setSizePolicy(sizePolicy)
        self.first_page_button.setMinimumSize(QSize(30, 30))
        self.first_page_button.setMaximumSize(QSize(45, 45))

        self.horizontalLayout_4.addWidget(self.first_page_button)

        self.second_page_button = QPushButton(self.pagination)
        self.second_page_button.setObjectName(u"second_page_button")
        sizePolicy.setHeightForWidth(self.second_page_button.sizePolicy().hasHeightForWidth())
        self.second_page_button.setSizePolicy(sizePolicy)
        self.second_page_button.setMinimumSize(QSize(30, 30))
        self.second_page_button.setMaximumSize(QSize(45, 45))

        self.horizontalLayout_4.addWidget(self.second_page_button)

        self.label_2 = QLabel(self.pagination)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(0, 45))

        self.horizontalLayout_4.addWidget(self.label_2)

        self.next_pagination_button = QPushButton(self.pagination)
        self.next_pagination_button.setObjectName(u"next_pagination_button")
        sizePolicy.setHeightForWidth(self.next_pagination_button.sizePolicy().hasHeightForWidth())
        self.next_pagination_button.setSizePolicy(sizePolicy)
        self.next_pagination_button.setMinimumSize(QSize(0, 45))

        self.horizontalLayout_4.addWidget(self.next_pagination_button)

        self.last_page_button = QPushButton(self.pagination)
        self.last_page_button.setObjectName(u"last_page_button")
        sizePolicy.setHeightForWidth(self.last_page_button.sizePolicy().hasHeightForWidth())
        self.last_page_button.setSizePolicy(sizePolicy)
        self.last_page_button.setMinimumSize(QSize(25, 45))

        self.horizontalLayout_4.addWidget(self.last_page_button)


        self.verticalLayout_3.addWidget(self.pagination)


        self.verticalLayout_2.addWidget(self.table_part)


        self.horizontalLayout.addWidget(self.main_part)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 957, 37))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.action_4)
        self.menu_2.addAction(self.action_5)
        self.menu_2.addAction(self.action_6)
        self.menu_3.addAction(self.action_7)
        self.menu_3.addAction(self.action_8)
        self.menu_3.addSeparator()
        self.menu_4.addAction(self.action_10)
        self.menu_4.addAction(self.action_11)
        self.menu_4.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0438\u0437 \u0444\u0430\u0439\u043b\u0430", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432 \u0444\u0430\u0439\u043b", None))
        self.action_4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
        self.action_5.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.action_6.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.action_7.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043c\u043d\u0430\u044f \u0442\u0435\u043c\u0430", None))
        self.action_8.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0432\u0435\u0442\u043b\u0430\u044f \u0442\u0435\u043c\u0430", None))
        self.action_10.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.action_11.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043c\u043e\u0449\u044c", None))
        self.app_label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u043e\u0440\u0442\u0423\u0447\u0435\u0442", None))
        self.add_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.delete_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.search_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.settings_button.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.table_name_label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u043e\u0440\u0442\u0441\u043c\u0435\u043d\u044b", None))
        self.file_name_label.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.load_button.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 1 \u0438\u0437 1", None))
        self.prev_pagination_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434.", None))
        self.first_page_button.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.second_page_button.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.next_pagination_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043b\u0435\u0434.", None))
        self.last_page_button.setText(QCoreApplication.translate("MainWindow", u">>", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0438\u0441\u0438", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0434", None))
        self.menu_4.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
    # retranslateUi


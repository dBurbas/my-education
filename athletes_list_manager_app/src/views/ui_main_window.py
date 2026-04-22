# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QSize(900, 600))
        MainWindow.setBaseSize(QSize(1100, 700))
        font = QFont()
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(
            "/*--------- General ---------*/\n"
            "QMainWindow {\n"
            "	background-color: palette(window);\n"
            "}\n"
            "QStatusBar {\n"
            "	background-color: palette(window);\n"
            "}\n"
            "QFrame#main_part {\n"
            "	background-color: palette(base);\n"
            '	font-family: "Inter", sans-serif;\n'
            "	font-size: 14pt;\n"
            "	border: none;\n"
            "}\n"
            "QFrame {\n"
            "	border:none;\n"
            "	color: palette(text);\n"
            "}\n"
            "QPushButton {\n"
            "	background-color: palette(button);\n"
            "	border-radius: 12%;\n"
            "	color: palette(button-text);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: palette(highlight);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "	background-color: #76f725;\n"
            "	color: #000000;\n"
            "}\n"
            "/*--------- Main part ---------*/\n"
            "QLabel#table_name_label {\n"
            '	font: 15pt "Inter";\n'
            "}\n"
            "QLabel#file_name_label {\n"
            '	font: 14pt "Inter";\n'
            "	color: palette(text);\n"
            "}\n"
            "QFrame#table_head {\n"
            "	background-color: palette(base);\n"
            "}\n"
            "QFrame#table_head QPushButton{\n"
            "	padding: 0 0.9em;\n"
            "	padding-left: 0.7em;\n"
            "	text-align:left;\n"
            "}\n"
            ""
            "QFrame#table_part {\n"
            "	border: 2px solid palette(midlight);\n"
            "	border-radius: 1em;\n"
            "	background-color: palette(base);\n"
            "	margin: 0 1em;\n"
            "}\n"
            "QFrame#table_part QFrame#pagination {\n"
            "	border-top: 2px solid palette(midlight);\n"
            "	border-bottom-left-radius: 10%;\n"
            "	border-bottom-right-radius: 10%;\n"
            "}\n"
            "QComboBox {\n"
            "    border: 2px solid palette(button); \n"
            "    border-radius: 7%;\n"
            "    padding: 2px 5px;\n"
            "}\n"
            "QComboBox::drop-down {\n"
            "    background-color: palette(alternate-base); \n"
            "    \n"
            "    border-left: 2px solid palette(midlight);\n"
            "    border-top-right-radius: 5%;\n"
            "    border-bottom-right-radius: 5%;\n"
            "    \n"
            "    width: 25px; \n"
            "}\n"
            "QComboBox::down-arrow {\n"
            '    image: url("/Users/dmitryburbas/Documents/Education/github_education_repo/my-education/athletes_list_manager_app/src/images/combo-icon.png");\n'
            "    width: 16px;\n"
            "    height: 16px;\n"
            "}\n"
            "QComboBox::drop-down:on {\n"
            "    background-color:#76f725;\n"
            "}\n"
            "QComboBox:focus {\n"
            "    borde"
            "r: 2px solid #76f725; \n"
            "}\n"
            "QComboBox::drop-down:disabled {\n"
            "    background-color:palette(button);\n"
            "}\n"
            "QComboBox:disabled {\n"
            "	background-color:palette(button);\n"
            "}\n"
            "\n"
            "QComboBox::drop-down:hover {\n"
            "    background-color:#76f725;\n"
            "}\n"
            "/*--------- Sidebar ---------*/\n"
            "QFrame#sidebar {\n"
            "	background-color: palette(base);\n"
            "	border-right: 2px solid palette(midlight);\n"
            "}\n"
            "QLabel#app_label {\n"
            '	font: bold italic 24pt "Gill Sans"; \n'
            "}\n"
            "QFrame#sidebar QPushButton {\n"
            "	background-color: palette(button);\n"
            "	border-top-left-radius: 0;\n"
            "	border-bottom-left-radius: 0;\n"
            "	border-top-right-radius: 1em;\n"
            "	border-bottom-right-radius: 1em;\n"
            "	font: 14pt;\n"
            "	text-align: left;\n"
            "	padding-left: 1.5em;\n"
            "}\n"
            "\n"
            "QFrame#sidebar QPushButton:hover {\n"
            "	background-color: palette(highlight);\n"
            "	color: palette(highlighted-text);\n"
            "	font-weight: bold;\n"
            "}\n"
            "QFrame#sidebar QPushButton:pressed {\n"
            "	background-color: #76f725;\n"
            "	color: #000000;\n"
            "	fo"
            "nt-weight: bold;\n"
            "}\n"
            "\n"
            ""
        )
        self.action_load = QAction(MainWindow)
        self.action_load.setObjectName("action_load")
        self.action_load.setIconVisibleInMenu(False)
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_add = QAction(MainWindow)
        self.action_add.setObjectName("action_add")
        self.action_delete = QAction(MainWindow)
        self.action_delete.setObjectName("action_delete")
        self.action_7 = QAction(MainWindow)
        self.action_7.setObjectName("action_7")
        self.action_8 = QAction(MainWindow)
        self.action_8.setObjectName("action_8")
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName("action_settings")
        self.action_help = QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.action_search = QAction(MainWindow)
        self.action_search.setObjectName("action_search")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setMinimumSize(QSize(225, 0))
        self.sidebar.setMaximumSize(QSize(250, 16777215))
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.sidebar)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_head = QFrame(self.sidebar)
        self.sidebar_head.setObjectName("sidebar_head")
        self.sidebar_head.setMinimumSize(QSize(0, 75))
        self.sidebar_head.setMaximumSize(QSize(16777215, 75))
        self.sidebar_head.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar_head.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.sidebar_head)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(15, 0, 15, 0)
        self.app_logo_label = QLabel(self.sidebar_head)
        self.app_logo_label.setObjectName("app_logo_label")
        self.app_logo_label.setMaximumSize(QSize(65, 65))
        self.app_logo_label.setPixmap(QPixmap("src/images/athlete_manager_logo.png"))
        self.app_logo_label.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.app_logo_label)

        self.app_label = QLabel(self.sidebar_head)
        self.app_label.setObjectName("app_label")
        font1 = QFont()
        font1.setFamilies(["Gill Sans"])
        font1.setPointSize(24)
        font1.setBold(True)
        font1.setItalic(True)
        self.app_label.setFont(font1)

        self.horizontalLayout_2.addWidget(self.app_label)

        self.verticalLayout.addWidget(self.sidebar_head)

        self.sidebar_buttons = QFrame(self.sidebar)
        self.sidebar_buttons.setObjectName("sidebar_buttons")
        self.sidebar_buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.sidebar_buttons)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 20, 15, 20)
        self.add_button = QPushButton(self.sidebar_buttons)
        self.add_button.setObjectName("add_button")
        self.add_button.setMinimumSize(QSize(0, 50))
        self.add_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_button.setMouseTracking(True)
        icon = QIcon(QIcon.fromTheme("document-new"))
        self.add_button.setIcon(icon)
        self.add_button.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.add_button)

        self.delete_button = QPushButton(self.sidebar_buttons)
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setMinimumSize(QSize(0, 50))
        self.delete_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.delete_button.setMouseTracking(True)
        icon1 = QIcon(QIcon.fromTheme("user-trash"))
        self.delete_button.setIcon(icon1)
        self.delete_button.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.delete_button)

        self.search_button = QPushButton(self.sidebar_buttons)
        self.search_button.setObjectName("search_button")
        self.search_button.setMinimumSize(QSize(0, 50))
        self.search_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.search_button.setMouseTracking(True)
        icon2 = QIcon(QIcon.fromTheme("system-search"))
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.search_button)

        self.buttons_spacer = QSpacerItem(
            20, 176, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_4.addItem(self.buttons_spacer)

        self.settings_button = QPushButton(self.sidebar_buttons)
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setMinimumSize(QSize(0, 50))
        self.settings_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_button.setMouseTracking(True)
        icon3 = QIcon(QIcon.fromTheme("applications-system"))
        self.settings_button.setIcon(icon3)
        self.settings_button.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.settings_button)

        self.verticalLayout.addWidget(self.sidebar_buttons)

        self.horizontalLayout.addWidget(self.sidebar)

        self.main_part = QFrame(self.centralwidget)
        self.main_part.setObjectName("main_part")
        self.main_part.setMinimumSize(QSize(650, 0))
        self.main_part.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_part.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.main_part)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 20)
        self.table_head = QFrame(self.main_part)
        self.table_head.setObjectName("table_head")
        self.table_head.setMinimumSize(QSize(0, 75))
        self.table_head.setMaximumSize(QSize(16777215, 75))
        self.table_head.setFrameShape(QFrame.Shape.StyledPanel)
        self.table_head.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.table_head)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(20, 5, 20, 5)
        self.table_name_label = QLabel(self.table_head)
        self.table_name_label.setObjectName("table_name_label")
        font2 = QFont()
        font2.setFamilies(["Inter"])
        font2.setPointSize(15)
        font2.setBold(False)
        font2.setItalic(False)
        self.table_name_label.setFont(font2)

        self.horizontalLayout_3.addWidget(self.table_name_label)

        self.table_head_spacer = QSpacerItem(
            128, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_3.addItem(self.table_head_spacer)

        self.table_head_divide = QFrame(self.table_head)
        self.table_head_divide.setObjectName("table_head_divide")
        self.table_head_divide.setFrameShape(QFrame.Shape.VLine)
        self.table_head_divide.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.table_head_divide)

        self.file_name_label = QLabel(self.table_head)
        self.file_name_label.setObjectName("file_name_label")
        font3 = QFont()
        font3.setFamilies(["Inter"])
        font3.setPointSize(14)
        font3.setBold(False)
        font3.setItalic(False)
        self.file_name_label.setFont(font3)

        self.horizontalLayout_3.addWidget(self.file_name_label)

        self.save_button = QPushButton(self.table_head)
        self.save_button.setObjectName("save_button")
        self.save_button.setMinimumSize(QSize(132, 40))
        font4 = QFont()
        font4.setPointSize(14)
        self.save_button.setFont(font4)
        self.save_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon(QIcon.fromTheme("document-save-as"))
        self.save_button.setIcon(icon4)
        self.save_button.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.save_button)

        self.load_button = QPushButton(self.table_head)
        self.load_button.setObjectName("load_button")
        self.load_button.setMinimumSize(QSize(128, 40))
        self.load_button.setFont(font4)
        self.load_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon(QIcon.fromTheme("folder"))
        self.load_button.setIcon(icon5)
        self.load_button.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.load_button)

        self.verticalLayout_2.addWidget(self.table_head)

        self.table_part = QFrame(self.main_part)
        self.table_part.setObjectName("table_part")
        self.table_part.setFrameShape(QFrame.Shape.StyledPanel)
        self.table_part.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.table_part)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.table_part)
        self.frame.setObjectName("frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 20))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_3.addWidget(self.frame)

        self.tableView = QTableView(self.table_part)
        self.tableView.setObjectName("tableView")

        self.verticalLayout_3.addWidget(self.tableView)

        self.pagination = QFrame(self.table_part)
        self.pagination.setObjectName("pagination")
        self.pagination.setMinimumSize(QSize(500, 50))
        self.pagination.setMaximumSize(QSize(16777215, 50))
        self.pagination.setFrameShape(QFrame.Shape.StyledPanel)
        self.pagination.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.pagination)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 5, 10, 5)
        self.current_page_label = QLabel(self.pagination)
        self.current_page_label.setObjectName("current_page_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.current_page_label.sizePolicy().hasHeightForWidth()
        )
        self.current_page_label.setSizePolicy(sizePolicy1)
        self.current_page_label.setMinimumSize(QSize(0, 40))
        self.current_page_label.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_4.addWidget(self.current_page_label)

        self.records_on_page_comboBox = QComboBox(self.pagination)
        self.records_on_page_comboBox.setObjectName("records_on_page_comboBox")
        self.records_on_page_comboBox.setMinimumSize(QSize(0, 25))
        self.records_on_page_comboBox.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_4.addWidget(self.records_on_page_comboBox)

        self.pagination_spacer_right = QSpacerItem(
            193, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_4.addItem(self.pagination_spacer_right)

        self.prev_pagination_button = QPushButton(self.pagination)
        self.prev_pagination_button.setObjectName("prev_pagination_button")
        sizePolicy1.setHeightForWidth(
            self.prev_pagination_button.sizePolicy().hasHeightForWidth()
        )
        self.prev_pagination_button.setSizePolicy(sizePolicy1)
        self.prev_pagination_button.setMinimumSize(QSize(40, 40))
        self.prev_pagination_button.setMaximumSize(QSize(40, 40))
        font5 = QFont()
        font5.setFamilies([".AppleSystemUIFont"])
        self.prev_pagination_button.setFont(font5)
        self.prev_pagination_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor)
        )
        icon6 = QIcon(QIcon.fromTheme("system-reboot"))
        self.prev_pagination_button.setIcon(icon6)

        self.horizontalLayout_4.addWidget(self.prev_pagination_button)

        self.first_page_button = QPushButton(self.pagination)
        self.first_page_button.setObjectName("first_page_button")
        sizePolicy1.setHeightForWidth(
            self.first_page_button.sizePolicy().hasHeightForWidth()
        )
        self.first_page_button.setSizePolicy(sizePolicy1)
        self.first_page_button.setMinimumSize(QSize(40, 40))
        self.first_page_button.setMaximumSize(QSize(40, 40))
        self.first_page_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_4.addWidget(self.first_page_button)

        self.second_page_button = QPushButton(self.pagination)
        self.second_page_button.setObjectName("second_page_button")
        sizePolicy1.setHeightForWidth(
            self.second_page_button.sizePolicy().hasHeightForWidth()
        )
        self.second_page_button.setSizePolicy(sizePolicy1)
        self.second_page_button.setMinimumSize(QSize(40, 40))
        self.second_page_button.setMaximumSize(QSize(40, 40))
        self.second_page_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_4.addWidget(self.second_page_button)

        self.pagination_ellipsis_label = QLabel(self.pagination)
        self.pagination_ellipsis_label.setObjectName("pagination_ellipsis_label")
        sizePolicy1.setHeightForWidth(
            self.pagination_ellipsis_label.sizePolicy().hasHeightForWidth()
        )
        self.pagination_ellipsis_label.setSizePolicy(sizePolicy1)
        self.pagination_ellipsis_label.setMinimumSize(QSize(40, 40))
        self.pagination_ellipsis_label.setMaximumSize(QSize(40, 40))
        self.pagination_ellipsis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.pagination_ellipsis_label)

        self.next_pagination_button = QPushButton(self.pagination)
        self.next_pagination_button.setObjectName("next_pagination_button")
        sizePolicy1.setHeightForWidth(
            self.next_pagination_button.sizePolicy().hasHeightForWidth()
        )
        self.next_pagination_button.setSizePolicy(sizePolicy1)
        self.next_pagination_button.setMinimumSize(QSize(40, 40))
        self.next_pagination_button.setMaximumSize(QSize(40, 40))
        self.next_pagination_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor)
        )
        icon7 = QIcon(QIcon.fromTheme("media-playback-start"))
        self.next_pagination_button.setIcon(icon7)

        self.horizontalLayout_4.addWidget(self.next_pagination_button)

        self.last_page_button = QPushButton(self.pagination)
        self.last_page_button.setObjectName("last_page_button")
        sizePolicy1.setHeightForWidth(
            self.last_page_button.sizePolicy().hasHeightForWidth()
        )
        self.last_page_button.setSizePolicy(sizePolicy1)
        self.last_page_button.setMinimumSize(QSize(40, 40))
        self.last_page_button.setMaximumSize(QSize(40, 40))
        self.last_page_button.setBaseSize(QSize(25, 25))
        self.last_page_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon8 = QIcon(QIcon.fromTheme("media-seek-forward"))
        self.last_page_button.setIcon(icon8)

        self.horizontalLayout_4.addWidget(self.last_page_button)

        self.verticalLayout_3.addWidget(self.pagination)

        self.verticalLayout_2.addWidget(self.table_part)

        self.horizontalLayout.addWidget(self.main_part)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 37))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_records = QMenu(self.menubar)
        self.menu_records.setObjectName("menu_records")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_records.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_load)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_records.addAction(self.action_add)
        self.menu_records.addAction(self.action_delete)
        self.menu_records.addAction(self.action_search)
        self.menu_help.addAction(self.action_settings)
        self.menu_help.addAction(self.action_help)
        self.menu_help.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.action_load.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0438\u0437 \u0444\u0430\u0439\u043b\u0430",
                None,
            )
        )
        self.action_save.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432 \u0444\u0430\u0439\u043b",
                None,
            )
        )
        self.action_exit.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0412\u044b\u0439\u0442\u0438", None
            )
        )
        self.action_add.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c",
                None,
            )
        )
        self.action_delete.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c",
                None,
            )
        )
        self.action_7.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0422\u0435\u043c\u043d\u0430\u044f \u0442\u0435\u043c\u0430",
                None,
            )
        )
        self.action_8.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u0432\u0435\u0442\u043b\u0430\u044f \u0442\u0435\u043c\u0430",
                None,
            )
        )
        self.action_settings.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438",
                None,
            )
        )
        self.action_help.setText(
            QCoreApplication.translate(
                "MainWindow", "\u041f\u043e\u043c\u043e\u0449\u044c", None
            )
        )
        self.action_search.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041f\u043e\u0438\u0441\u043a \u0437\u0430\u043f\u0438\u0441\u0435\u0439",
                None,
            )
        )
        self.app_logo_label.setText("")
        self.app_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p>Sport<span style=" font-style:normal; color:#76f725;">Man</span></p></body></html>',
                None,
            )
        )
        self.add_button.setText(
            QCoreApplication.translate(
                "MainWindow", " \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None
            )
        )
        self.delete_button.setText(
            QCoreApplication.translate(
                "MainWindow", " \u0423\u0434\u0430\u043b\u0438\u0442\u044c", None
            )
        )
        self.search_button.setText(
            QCoreApplication.translate(
                "MainWindow", " \u041f\u043e\u0438\u0441\u043a", None
            )
        )
        self.settings_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                " \u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438",
                None,
            )
        )
        self.table_name_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0441\u043f\u043e\u0440\u0442\u0441\u043c\u0435\u043d\u043e\u0432",
                None,
            )
        )
        self.file_name_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0424\u0430\u0439\u043b \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d",
                None,
            )
        )
        self.save_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                " \u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
                None,
            )
        )
        self.load_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                " \u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c",
                None,
            )
        )
        self.current_page_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 1 \u0438\u0437 1",
                None,
            )
        )
        self.prev_pagination_button.setText("")
        self.first_page_button.setText(
            QCoreApplication.translate("MainWindow", "1", None)
        )
        self.second_page_button.setText(
            QCoreApplication.translate("MainWindow", "2", None)
        )
        self.pagination_ellipsis_label.setText(
            QCoreApplication.translate("MainWindow", "...", None)
        )
        self.next_pagination_button.setText("")
        self.last_page_button.setText("")
        self.menu_file.setTitle(
            QCoreApplication.translate("MainWindow", "\u0424\u0430\u0439\u043b", None)
        )
        self.menu_records.setTitle(
            QCoreApplication.translate(
                "MainWindow", "\u0417\u0430\u043f\u0438\u0441\u0438", None
            )
        )
        self.menu_help.setTitle(
            QCoreApplication.translate(
                "MainWindow", "\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None
            )
        )

    # retranslateUi

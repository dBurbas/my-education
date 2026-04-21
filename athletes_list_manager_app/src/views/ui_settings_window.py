# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGroupBox, QRadioButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(300, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        Settings.setMinimumSize(QSize(300, 200))
        Settings.setMaximumSize(QSize(300, 150))
        Settings.setStyleSheet(u"QMainWindow {\n"
"	background-color: palette(window);\n"
"}\n"
"QStatusBar {\n"
"	background-color: palette(window);\n"
"}\n"
"QGroupBox {\n"
"	background: None;\n"
"	font-family: \"Inter\", sans-serif;\n"
"	font-size: 14pt;\n"
"}\n"
"QRadioButton {\n"
"    color: palette(highlighted-text); \n"
"    font-weight: normal;\n"
"}\n"
"\n"
"QRadioButton:checked {\n"
"	color: palette(highlighted-text);\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.appearance_groupBox = QGroupBox(Settings)
        self.appearance_groupBox.setObjectName(u"appearance_groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.appearance_groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 5)
        self.theme_groupBox = QGroupBox(self.appearance_groupBox)
        self.theme_groupBox.setObjectName(u"theme_groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.theme_groupBox.sizePolicy().hasHeightForWidth())
        self.theme_groupBox.setSizePolicy(sizePolicy1)
        self.theme_groupBox.setMaximumSize(QSize(16777215, 120))
        self.verticalLayout_3 = QVBoxLayout(self.theme_groupBox)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.system_theme_radioButton = QRadioButton(self.theme_groupBox)
        self.system_theme_radioButton.setObjectName(u"system_theme_radioButton")
        font = QFont()
        font.setBold(False)
        self.system_theme_radioButton.setFont(font)

        self.verticalLayout_3.addWidget(self.system_theme_radioButton)

        self.dark_theme_radioButton = QRadioButton(self.theme_groupBox)
        self.dark_theme_radioButton.setObjectName(u"dark_theme_radioButton")

        self.verticalLayout_3.addWidget(self.dark_theme_radioButton)

        self.light_theme_radioButton = QRadioButton(self.theme_groupBox)
        self.light_theme_radioButton.setObjectName(u"light_theme_radioButton")

        self.verticalLayout_3.addWidget(self.light_theme_radioButton)


        self.verticalLayout_2.addWidget(self.theme_groupBox)


        self.verticalLayout.addWidget(self.appearance_groupBox)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Dialog", None))
        self.appearance_groupBox.setTitle(QCoreApplication.translate("Settings", u"\u0412\u043d\u0435\u0448\u043d\u0438\u0439 \u0432\u0438\u0434", None))
        self.theme_groupBox.setTitle(QCoreApplication.translate("Settings", u"\u0422\u0435\u043c\u0430", None))
        self.system_theme_radioButton.setText(QCoreApplication.translate("Settings", u"\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u0430\u044f (Auto)", None))
        self.dark_theme_radioButton.setText(QCoreApplication.translate("Settings", u"\u0422\u0435\u043c\u043d\u0430\u044f", None))
        self.light_theme_radioButton.setText(QCoreApplication.translate("Settings", u"\u0421\u0432\u0435\u0442\u043b\u0430\u044f", None))
    # retranslateUi


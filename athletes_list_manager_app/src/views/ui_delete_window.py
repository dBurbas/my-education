# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'delete_window.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_DeleteDialog(object):
    def setupUi(self, DeleteDialog):
        if not DeleteDialog.objectName():
            DeleteDialog.setObjectName(u"DeleteDialog")
        DeleteDialog.resize(400, 570)
        DeleteDialog.setMinimumSize(QSize(400, 570))
        DeleteDialog.setStyleSheet(u" QDialog {\n"
"	background-color: palette(window);\n"
"}\n"
"QLabel {\n"
"	margin-left: 0.1em;\n"
"}\n"
"QFrame {\n"
"	border:none;\n"
"	color: palette(text);\n"
"}\n"
"QFrame#fields {\n"
"	background-color: palette(base);\n"
"	border-radius: 15%;\n"
"	border: 2px solid palette(button);\n"
"}\n"
"QPushButton {\n"
"	padding:10px;\n"
"	background-color: palette(base) ;\n"
"	border-radius: 12%;\n"
"	color: palette(button-text);\n"
"}\n"
"QLineEdit {\n"
"	border-radius: 7%;\n"
"	padding: 0 0.4em;\n"
"	background-color: palette(button);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid #76f725; \n"
"}\n"
"QSpinBox {\n"
"	border-radius: 7%;\n"
"	padding: 0.2em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: palette(highlight);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: #76f725;\n"
"	color: palette(shadow);\n"
"}\n"
"QComboBox {\n"
"    border: 2px solid palette(button); \n"
"    border-radius: 7%;\n"
"    padding: 2px 5px;\n"
"}\n"
"QComboBox::drop-down {\n"
"    background-color: palette(alternat"
                        "e-base); \n"
"    \n"
"    border-left: 2px solid palette(midlight);\n"
"    border-top-right-radius: 5%;\n"
"    border-bottom-right-radius: 5%;\n"
"    \n"
"    width: 25px; \n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(\"/Users/dmitryburbas/Documents/Education/github_education_repo/my-education/athletes_list_manager_app/src/images/combo-icon.png\");\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QComboBox::drop-down:on {\n"
"    background-color:#76f725;\n"
"}\n"
"QComboBox:focus {\n"
"    border: 2px solid #76f725; \n"
"}\n"
"QComboBox::drop-down:disabled {\n"
"    background-color:palette(button);\n"
"}\n"
"QComboBox:disabled {\n"
"	background-color:palette(button);\n"
"}\n"
"\n"
"\n"
"QComboBox::drop-down:hover {\n"
"    background-color:#76f725;\n"
"}\n"
"QSpinBox {\n"
"    padding-right: 15px;\n"
"	padding-left: 0.3em;\n"
"    border: 1px solid palette(midlight);\n"
"    border-radius: 7%;\n"
"    background-color: palette(base);\n"
"    color: palette(text);\n"
"}\n"
"\n"
"QSpinBox::up-b"
                        "utton {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right; \n"
"    width: 25px; \n"
"    \n"
"    background-color: palette(alternate-base);\n"
"    border-left: 1px solid  palette(base);\n"
"    border-top-right-radius: 5%;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 25px;\n"
"    \n"
"    background-color: palette(alternate-base);\n"
"	border-top: 1px solid  palette(base);\n"
"    border-left: 1px solid palette(base);\n"
"    border-bottom-right-radius: 5%;\n"
"}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    image: url(\"/Users/dmitryburbas/Documents/Education/github_education_repo/my-education/athletes_list_manager_app/src/images/up-arrow.png\");\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(\"/Users/dmitryburbas/Documents/Education/github_education_repo/my-education/athletes_list_manager_app/src/images/down-arrow.png\");\n"
"    width: 14px;\n"
"    "
                        "height: 14px;\n"
"}\n"
"QSpinBox::up-button:hover,QSpinBox::down-button:hover {\n"
"    background-color: #76f725;\n"
"}\n"
"QSpinBox::up-button:pressed,QSpinBox::down-button:pressed {\n"
"    background-color: #48b007;\n"
"}")
        self.horizontalLayout = QHBoxLayout(DeleteDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 50, 0)
        self.sidebar = QFrame(DeleteDialog)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(400, 570))
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.sidebar)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.fields = QFrame(self.sidebar)
        self.fields.setObjectName(u"fields")
        self.fields.setMinimumSize(QSize(0, 300))
        self.fields.setFrameShape(QFrame.Shape.StyledPanel)
        self.fields.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.fields)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 15)
        self.names = QFrame(self.fields)
        self.names.setObjectName(u"names")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.names.sizePolicy().hasHeightForWidth())
        self.names.setSizePolicy(sizePolicy)
        self.names.setMinimumSize(QSize(0, 230))
        self.names.setFrameShape(QFrame.Shape.StyledPanel)
        self.names.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.names)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.last_name = QFrame(self.names)
        self.last_name.setObjectName(u"last_name")
        self.last_name.setFrameShape(QFrame.Shape.StyledPanel)
        self.last_name.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.last_name)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.last_name_label = QLabel(self.last_name)
        self.last_name_label.setObjectName(u"last_name_label")

        self.verticalLayout_8.addWidget(self.last_name_label)

        self.last_name_lineEdit = QLineEdit(self.last_name)
        self.last_name_lineEdit.setObjectName(u"last_name_lineEdit")
        self.last_name_lineEdit.setMinimumSize(QSize(0, 30))

        self.verticalLayout_8.addWidget(self.last_name_lineEdit)


        self.verticalLayout_3.addWidget(self.last_name)

        self.first_name = QFrame(self.names)
        self.first_name.setObjectName(u"first_name")
        self.first_name.setFrameShape(QFrame.Shape.StyledPanel)
        self.first_name.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.first_name)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.first_name_label = QLabel(self.first_name)
        self.first_name_label.setObjectName(u"first_name_label")

        self.verticalLayout_6.addWidget(self.first_name_label)

        self.first_name_lineEdit = QLineEdit(self.first_name)
        self.first_name_lineEdit.setObjectName(u"first_name_lineEdit")
        self.first_name_lineEdit.setMinimumSize(QSize(0, 30))

        self.verticalLayout_6.addWidget(self.first_name_lineEdit)


        self.verticalLayout_3.addWidget(self.first_name)

        self.patronymic = QFrame(self.names)
        self.patronymic.setObjectName(u"patronymic")
        self.patronymic.setFrameShape(QFrame.Shape.StyledPanel)
        self.patronymic.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.patronymic)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.patronymic_label = QLabel(self.patronymic)
        self.patronymic_label.setObjectName(u"patronymic_label")

        self.verticalLayout_7.addWidget(self.patronymic_label)

        self.patronymic_lineEdit = QLineEdit(self.patronymic)
        self.patronymic_lineEdit.setObjectName(u"patronymic_lineEdit")
        self.patronymic_lineEdit.setMinimumSize(QSize(0, 30))

        self.verticalLayout_7.addWidget(self.patronymic_lineEdit)


        self.verticalLayout_3.addWidget(self.patronymic)


        self.verticalLayout_2.addWidget(self.names)

        self.title_count = QFrame(self.fields)
        self.title_count.setObjectName(u"title_count")
        self.title_count.setFrameShape(QFrame.Shape.StyledPanel)
        self.title_count.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.title_count)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(12, 0, 12, 0)
        self.min_title = QFrame(self.title_count)
        self.min_title.setObjectName(u"min_title")
        self.min_title.setFrameShape(QFrame.Shape.StyledPanel)
        self.min_title.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.min_title)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.min_label = QLabel(self.min_title)
        self.min_label.setObjectName(u"min_label")

        self.verticalLayout_4.addWidget(self.min_label)

        self.min_spinBox = QSpinBox(self.min_title)
        self.min_spinBox.setObjectName(u"min_spinBox")
        self.min_spinBox.setMaximum(999)

        self.verticalLayout_4.addWidget(self.min_spinBox)


        self.gridLayout.addWidget(self.min_title, 1, 1, 1, 1)

        self.max_title = QFrame(self.title_count)
        self.max_title.setObjectName(u"max_title")
        self.max_title.setFrameShape(QFrame.Shape.StyledPanel)
        self.max_title.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.max_title)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.max_label = QLabel(self.max_title)
        self.max_label.setObjectName(u"max_label")

        self.verticalLayout_5.addWidget(self.max_label)

        self.max_spinBox = QSpinBox(self.max_title)
        self.max_spinBox.setObjectName(u"max_spinBox")
        self.max_spinBox.setMaximum(999)

        self.verticalLayout_5.addWidget(self.max_spinBox)


        self.gridLayout.addWidget(self.max_title, 1, 2, 1, 1)

        self.title_count_label = QLabel(self.title_count)
        self.title_count_label.setObjectName(u"title_count_label")

        self.gridLayout.addWidget(self.title_count_label, 0, 1, 1, 2)


        self.verticalLayout_2.addWidget(self.title_count)

        self.sport_type = QFrame(self.fields)
        self.sport_type.setObjectName(u"sport_type")
        self.sport_type.setFrameShape(QFrame.Shape.StyledPanel)
        self.sport_type.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.sport_type)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, 0, -1, 0)
        self.sport_label = QLabel(self.sport_type)
        self.sport_label.setObjectName(u"sport_label")

        self.verticalLayout_9.addWidget(self.sport_label)

        self.sport_comboBox = QComboBox(self.sport_type)
        self.sport_comboBox.setObjectName(u"sport_comboBox")

        self.verticalLayout_9.addWidget(self.sport_comboBox)


        self.verticalLayout_2.addWidget(self.sport_type)

        self.athlete_category = QFrame(self.fields)
        self.athlete_category.setObjectName(u"athlete_category")
        self.athlete_category.setFrameShape(QFrame.Shape.StyledPanel)
        self.athlete_category.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.athlete_category)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(-1, 0, -1, 0)
        self.category_label = QLabel(self.athlete_category)
        self.category_label.setObjectName(u"category_label")

        self.verticalLayout_10.addWidget(self.category_label)

        self.category_comboBox = QComboBox(self.athlete_category)
        self.category_comboBox.setObjectName(u"category_comboBox")

        self.verticalLayout_10.addWidget(self.category_comboBox)


        self.verticalLayout_2.addWidget(self.athlete_category)


        self.verticalLayout_11.addWidget(self.fields)

        self.buttonBox = QDialogButtonBox(self.sidebar)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setKerning(True)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_11.addWidget(self.buttonBox)

        self.verticalSpacer = QSpacerItem(20, 31, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.sidebar)


        self.retranslateUi(DeleteDialog)
        self.buttonBox.accepted.connect(DeleteDialog.accept)
        self.buttonBox.rejected.connect(DeleteDialog.reject)

        QMetaObject.connectSlotsByName(DeleteDialog)
    # setupUi

    def retranslateUi(self, DeleteDialog):
        DeleteDialog.setWindowTitle(QCoreApplication.translate("DeleteDialog", u"Dialog", None))
        self.last_name_label.setText(QCoreApplication.translate("DeleteDialog", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None))
        self.first_name_label.setText(QCoreApplication.translate("DeleteDialog", u"\u0418\u043c\u044f", None))
        self.patronymic_label.setText(QCoreApplication.translate("DeleteDialog", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.min_label.setText(QCoreApplication.translate("DeleteDialog", u"\u041c\u0438\u043d\u0438\u043c\u0443\u043c", None))
        self.max_label.setText(QCoreApplication.translate("DeleteDialog", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c", None))
        self.title_count_label.setText(QCoreApplication.translate("DeleteDialog", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0437\u0430\u0432\u043e\u0435\u0432\u0430\u043d\u0438\u0439 \u0442\u0438\u0442\u0443\u043b\u043e\u0432", None))
        self.sport_label.setText(QCoreApplication.translate("DeleteDialog", u"\u0412\u0438\u0434 \u0441\u043f\u043e\u0440\u0442\u0430", None))
        self.category_label.setText(QCoreApplication.translate("DeleteDialog", u"\u0420\u0430\u0437\u0440\u044f\u0434", None))
    # retranslateUi


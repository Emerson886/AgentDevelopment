# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PCB_System_2.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTableView, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 635)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet(u"font: 14pt \"Arial\";")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_11 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.main_widget = QWidget(self.centralwidget)
        self.main_widget.setObjectName(u"main_widget")
        self.main_widget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.main_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_selections = QWidget(self.main_widget)
        self.widget_selections.setObjectName(u"widget_selections")
        self.widget_selections.setMinimumSize(QSize(200, 0))
        self.widget_selections.setMaximumSize(QSize(250, 16777215))
        self.widget_selections.setFont(font)
        self.widget_selections.setStyleSheet(u"background-color: rgb(35, 41, 46);\n"
"color: rgb(255, 255, 255);")
        self.verticalLayout_18 = QVBoxLayout(self.widget_selections)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.widget_left = QWidget(self.widget_selections)
        self.widget_left.setObjectName(u"widget_left")
        self.widget_left.setMinimumSize(QSize(0, 500))
        self.widget_left.setMaximumSize(QSize(16777215, 500))
        self.verticalLayout_19 = QVBoxLayout(self.widget_left)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.widget_title = QWidget(self.widget_left)
        self.widget_title.setObjectName(u"widget_title")
        self.widget_title.setMaximumSize(QSize(16777215, 120))
        self.widget_title.setStyleSheet(u"color: rgb(30, 159, 255);\n"
"font: 17pt \"SimSun\";\n"
"font-weight:bold;")
        self.verticalLayout_17 = QVBoxLayout(self.widget_title)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.widget_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamilies([u"SimSun"])
        font1.setPointSize(17)
        font1.setBold(True)
        font1.setItalic(False)
        self.label_title.setFont(font1)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setWordWrap(True)

        self.verticalLayout_17.addWidget(self.label_title)


        self.verticalLayout_19.addWidget(self.widget_title)

        self.line = QFrame(self.widget_left)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"background-color: rgb(194, 194, 194);")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_19.addWidget(self.line)

        self.widget_bts_selection = QWidget(self.widget_left)
        self.widget_bts_selection.setObjectName(u"widget_bts_selection")
        self.widget_bts_selection.setMaximumSize(QSize(16777215, 300))
        self.widget_bts_selection.setStyleSheet(u"QPushButton {\n"
"                min-width: 0px;\n"
"			  min-height: 60px;\n"
"                border: none;\n"
"                color: white;\n"
"                font-size: 20px;\n"
"		       font-weight: bold;\n"
"            }\n"
"")
        self.verticalLayout_9 = QVBoxLayout(self.widget_bts_selection)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.bt_dt_Stage = QPushButton(self.widget_bts_selection)
        self.bt_dt_Stage.setObjectName(u"bt_dt_Stage")
        self.bt_dt_Stage.setMinimumSize(QSize(0, 60))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setBold(True)
        font2.setItalic(False)
        self.bt_dt_Stage.setFont(font2)
        self.bt_dt_Stage.setStyleSheet(u"QPushButton:hover{\n"
"	background-color: rgb(47, 54, 60);\n"
"}")
        self.bt_dt_Stage.setCheckable(False)
        self.bt_dt_Stage.setChecked(False)
        self.bt_dt_Stage.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.bt_dt_Stage)

        self.btn_history = QPushButton(self.widget_bts_selection)
        self.btn_history.setObjectName(u"btn_history")
        self.btn_history.setFont(font2)
        self.btn_history.setStyleSheet(u"QPushButton:hover{\n"
"	background-color: rgb(47, 54, 60);\n"
"}")
        self.btn_history.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.btn_history)

        self.btn_AI = QPushButton(self.widget_bts_selection)
        self.btn_AI.setObjectName(u"btn_AI")
        self.btn_AI.setStyleSheet(u"QPushButton:hover{\n"
"	background-color: rgb(47, 54, 60);\n"
"}")

        self.verticalLayout_9.addWidget(self.btn_AI)

        self.btn_params = QPushButton(self.widget_bts_selection)
        self.btn_params.setObjectName(u"btn_params")
        self.btn_params.setStyleSheet(u"QPushButton:hover{\n"
"	background-color: rgb(47, 54, 60);\n"
"}")
        self.btn_params.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.btn_params)

        self.btn_exit = QPushButton(self.widget_bts_selection)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setStyleSheet(u"QPushButton:hover{\n"
"	background-color: rgb(47, 54, 60);\n"
"}")
        self.btn_exit.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.btn_exit)


        self.verticalLayout_19.addWidget(self.widget_bts_selection)


        self.verticalLayout_18.addWidget(self.widget_left)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_18.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget_selections)

        self.tabWidget = QTabWidget(self.main_widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setIconSize(QSize(16, 16))
        self.tabWidget.setUsesScrollButtons(True)
        self.tab_detection = QWidget()
        self.tab_detection.setObjectName(u"tab_detection")
        self.verticalLayout_7 = QVBoxLayout(self.tab_detection)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_input_area = QWidget(self.tab_detection)
        self.widget_input_area.setObjectName(u"widget_input_area")
        self.widget_input_area.setMaximumSize(QSize(16777215, 80))
        self.widget_input_area.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_input_area)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_input = QWidget(self.widget_input_area)
        self.widget_input.setObjectName(u"widget_input")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_input)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lb_input = QLabel(self.widget_input)
        self.lb_input.setObjectName(u"lb_input")
        self.lb_input.setFont(font)

        self.horizontalLayout_6.addWidget(self.lb_input)

        self.comboBox = QComboBox(self.widget_input)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.comboBox)


        self.horizontalLayout_3.addWidget(self.widget_input)

        self.widget_file_in = QWidget(self.widget_input_area)
        self.widget_file_in.setObjectName(u"widget_file_in")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_file_in)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_path_in = QLineEdit(self.widget_file_in)
        self.lineEdit_path_in.setObjectName(u"lineEdit_path_in")

        self.gridLayout.addWidget(self.lineEdit_path_in, 0, 0, 1, 1)

        self.input_fileBrowser = QPushButton(self.widget_file_in)
        self.input_fileBrowser.setObjectName(u"input_fileBrowser")
        self.input_fileBrowser.setFont(font)
        self.input_fileBrowser.setStyleSheet(u"QPushButton{ \n"
"	border:1px solid #16baaa;\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgb(22, 186, 170);\n"
"}")
        self.input_fileBrowser.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.input_fileBrowser, 0, 1, 1, 1)


        self.horizontalLayout_7.addLayout(self.gridLayout)


        self.horizontalLayout_3.addWidget(self.widget_file_in)

        self.widget_camr = QWidget(self.widget_input_area)
        self.widget_camr.setObjectName(u"widget_camr")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_camr)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.gridLayout_camr = QGridLayout()
        self.gridLayout_camr.setObjectName(u"gridLayout_camr")
        self.label_camr = QLabel(self.widget_camr)
        self.label_camr.setObjectName(u"label_camr")

        self.gridLayout_camr.addWidget(self.label_camr, 0, 0, 1, 1)

        self.btn_camr = QPushButton(self.widget_camr)
        self.btn_camr.setObjectName(u"btn_camr")
        self.btn_camr.setStyleSheet(u"background-color: rgb(22, 183, 119);")

        self.gridLayout_camr.addWidget(self.btn_camr, 0, 1, 1, 1)


        self.horizontalLayout_8.addLayout(self.gridLayout_camr)


        self.horizontalLayout_3.addWidget(self.widget_camr)


        self.verticalLayout_7.addWidget(self.widget_input_area)

        self.widget_pic = QWidget(self.tab_detection)
        self.widget_pic.setObjectName(u"widget_pic")
        self.widget_pic.setStyleSheet(u"color: rgb(194, 194, 194);")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_pic)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_originPic = QWidget(self.widget_pic)
        self.widget_originPic.setObjectName(u"widget_originPic")
        self.widget_originPic.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_2 = QVBoxLayout(self.widget_originPic)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_origin = QTabWidget(self.widget_originPic)
        self.tabWidget_origin.setObjectName(u"tabWidget_origin")
        self.pic_o = QWidget()
        self.pic_o.setObjectName(u"pic_o")
        self.verticalLayout_4 = QVBoxLayout(self.pic_o)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_o = QLabel(self.pic_o)
        self.label_o.setObjectName(u"label_o")
        self.label_o.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_o)

        self.tabWidget_origin.addTab(self.pic_o, "")
        self.video_o = QWidget()
        self.video_o.setObjectName(u"video_o")
        self.tabWidget_origin.addTab(self.video_o, "")
        self.camr_o = QWidget()
        self.camr_o.setObjectName(u"camr_o")
        self.tabWidget_origin.addTab(self.camr_o, "")

        self.verticalLayout_2.addWidget(self.tabWidget_origin)


        self.horizontalLayout_2.addWidget(self.widget_originPic)

        self.widget_detectPic = QWidget(self.widget_pic)
        self.widget_detectPic.setObjectName(u"widget_detectPic")
        self.widget_detectPic.setFont(font)
        self.widget_detectPic.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.verticalLayout_3 = QVBoxLayout(self.widget_detectPic)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_detect = QTabWidget(self.widget_detectPic)
        self.tabWidget_detect.setObjectName(u"tabWidget_detect")
        self.pic_d = QWidget()
        self.pic_d.setObjectName(u"pic_d")
        self.verticalLayout_5 = QVBoxLayout(self.pic_d)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_d = QLabel(self.pic_d)
        self.label_d.setObjectName(u"label_d")
        self.label_d.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_d)

        self.tabWidget_detect.addTab(self.pic_d, "")
        self.video_d = QWidget()
        self.video_d.setObjectName(u"video_d")
        self.tabWidget_detect.addTab(self.video_d, "")
        self.camr_d = QWidget()
        self.camr_d.setObjectName(u"camr_d")
        self.tabWidget_detect.addTab(self.camr_d, "")

        self.verticalLayout_3.addWidget(self.tabWidget_detect)


        self.horizontalLayout_2.addWidget(self.widget_detectPic)


        self.verticalLayout_7.addWidget(self.widget_pic)

        self.widget_sav_dt = QWidget(self.tab_detection)
        self.widget_sav_dt.setObjectName(u"widget_sav_dt")
        self.widget_sav_dt.setMaximumSize(QSize(16777215, 80))
        self.widget_sav_dt.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.horizontalLayout_5 = QHBoxLayout(self.widget_sav_dt)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widget_hint = QWidget(self.widget_sav_dt)
        self.widget_hint.setObjectName(u"widget_hint")
        self.widget_hint.setStyleSheet(u"font: 12pt \"Arial\";")
        self.verticalLayout_8 = QVBoxLayout(self.widget_hint)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.lb_hint = QLabel(self.widget_hint)
        self.lb_hint.setObjectName(u"lb_hint")
        self.lb_hint.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.lb_hint)


        self.horizontalLayout_5.addWidget(self.widget_hint)

        self.widget_bts_sd = QWidget(self.widget_sav_dt)
        self.widget_bts_sd.setObjectName(u"widget_bts_sd")
        self.widget_bts_sd.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.widget_bts_sd)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.bt_video_control = QPushButton(self.widget_bts_sd)
        self.bt_video_control.setObjectName(u"bt_video_control")
        self.bt_video_control.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(30, 159, 255);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgb(22, 120, 50);\n"
"}")

        self.horizontalLayout_4.addWidget(self.bt_video_control)

        self.bt_save = QPushButton(self.widget_bts_sd)
        self.bt_save.setObjectName(u"bt_save")
        self.bt_save.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(22, 186, 170);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgb(22, 120, 50);\n"
"}")

        self.horizontalLayout_4.addWidget(self.bt_save)

        self.bt_detect = QPushButton(self.widget_bts_sd)
        self.bt_detect.setObjectName(u"bt_detect")
        self.bt_detect.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(22, 183, 119);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgb(22, 120, 0);\n"
"}")

        self.horizontalLayout_4.addWidget(self.bt_detect)


        self.horizontalLayout_5.addWidget(self.widget_bts_sd)


        self.verticalLayout_7.addWidget(self.widget_sav_dt)

        self.widget_result = QWidget(self.tab_detection)
        self.widget_result.setObjectName(u"widget_result")
        self.widget_result.setMinimumSize(QSize(0, 100))
        self.widget_result.setMaximumSize(QSize(16777215, 200))
        self.widget_result.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font: 10pt \"Arial\";")
        self.verticalLayout_20 = QVBoxLayout(self.widget_result)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.text_results = QPlainTextEdit(self.widget_result)
        self.text_results.setObjectName(u"text_results")

        self.verticalLayout_20.addWidget(self.text_results)


        self.verticalLayout_7.addWidget(self.widget_result)

        self.tabWidget.addTab(self.tab_detection, "")
        self.tab_history = QWidget()
        self.tab_history.setObjectName(u"tab_history")
        self.verticalLayout_11 = QVBoxLayout(self.tab_history)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.tableView_history = QTableView(self.tab_history)
        self.tableView_history.setObjectName(u"tableView_history")
        self.tableView_history.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.tableView_history.horizontalHeader().setVisible(True)
        self.tableView_history.verticalHeader().setVisible(True)

        self.verticalLayout_11.addWidget(self.tableView_history)

        self.widget_save = QWidget(self.tab_history)
        self.widget_save.setObjectName(u"widget_save")
        self.widget_save.setStyleSheet(u"")
        self.verticalLayout_10 = QVBoxLayout(self.widget_save)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.gridLayout_save = QGridLayout()
        self.gridLayout_save.setObjectName(u"gridLayout_save")
        self.label_save = QLabel(self.widget_save)
        self.label_save.setObjectName(u"label_save")

        self.gridLayout_save.addWidget(self.label_save, 0, 0, 1, 1)

        self.lineEdit_path_out = QLineEdit(self.widget_save)
        self.lineEdit_path_out.setObjectName(u"lineEdit_path_out")

        self.gridLayout_save.addWidget(self.lineEdit_path_out, 0, 1, 1, 1)

        self.output_fileBrowser = QPushButton(self.widget_save)
        self.output_fileBrowser.setObjectName(u"output_fileBrowser")
        self.output_fileBrowser.setStyleSheet(u"QPushButton{ \n"
"	border:1px solid #16baaa;\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgb(22, 186, 170);\n"
"}")

        self.gridLayout_save.addWidget(self.output_fileBrowser, 0, 2, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout_save)


        self.verticalLayout_11.addWidget(self.widget_save)

        self.tabWidget.addTab(self.tab_history, "")
        self.tab_AI = QWidget()
        self.tab_AI.setObjectName(u"tab_AI")
        self.verticalLayout = QVBoxLayout(self.tab_AI)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_model_hint = QWidget(self.tab_AI)
        self.widget_model_hint.setObjectName(u"widget_model_hint")
        self.widget_model_hint.setStyleSheet(u"background-color:#1e9fff;")
        self.horizontalLayout_12 = QHBoxLayout(self.widget_model_hint)
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(9, 9, 9, 9)
        self.lb_AI_name = QLabel(self.widget_model_hint)
        self.lb_AI_name.setObjectName(u"lb_AI_name")
        self.lb_AI_name.setStyleSheet(u"color: rgb(255,255,255);")

        self.horizontalLayout_12.addWidget(self.lb_AI_name)

        self.horizontalSpacer_2 = QSpacerItem(364, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_2)

        self.btn_init_model = QPushButton(self.widget_model_hint)
        self.btn_init_model.setObjectName(u"btn_init_model")
        self.btn_init_model.setMinimumSize(QSize(85, 35))
        self.btn_init_model.setStyleSheet(u"\n"
"QPushButton:pressed{\n"
"	color: rgb(210, 210, 210);\n"
"}\n"
"QPushButton {\n"
"                background-color: #1e9fff;\n"
"                color: white;\n"
"                border: none;\n"
"                border-radius: 4px;\n"
"                font-size: 16px;\n"
"            }")

        self.horizontalLayout_12.addWidget(self.btn_init_model)


        self.verticalLayout.addWidget(self.widget_model_hint)

        self.scrollArea = QScrollArea(self.tab_AI)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 572, 266))
        self.scrollAreaWidgetContents.setAutoFillBackground(False)
        self.scrollAreaWidgetContents.setStyleSheet(u"background-color: #F5F5F5")
        self.verticalLayout_22 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.widget_input_text = QWidget(self.tab_AI)
        self.widget_input_text.setObjectName(u"widget_input_text")
        self.widget_input_text.setMaximumSize(QSize(16777215, 150))
        self.widget_input_text.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.widget_input_text.setStyleSheet(u"background-color: white")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_input_text)
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(14, 9, 14, 9)
        self.textEdit_question = QTextEdit(self.widget_input_text)
        self.textEdit_question.setObjectName(u"textEdit_question")
        self.textEdit_question.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.textEdit_question.setStyleSheet(u"border: none;")

        self.horizontalLayout_10.addWidget(self.textEdit_question)


        self.verticalLayout.addWidget(self.widget_input_text)

        self.widget_send = QWidget(self.tab_AI)
        self.widget_send.setObjectName(u"widget_send")
        self.widget_send.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.widget_send.setAutoFillBackground(False)
        self.widget_send.setStyleSheet(u"background-color:white")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_send)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.btn_send = QPushButton(self.widget_send)
        self.btn_send.setObjectName(u"btn_send")
        self.btn_send.setMinimumSize(QSize(80, 32))
        self.btn_send.setMaximumSize(QSize(80, 32))
        self.btn_send.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_send.setStyleSheet(u"QPushButton:pressed{\n"
"	background-color: rgb(109, 143, 205);\n"
"}\nQPushButton {\n"
"                background-color: rgb(30, 159, 255);;\n"
"                color: white;\n"
"                border: none;\n"
"                border-radius: 4px;\n"
"                font-size: 16px;\n"
"            }")

        self.horizontalLayout_9.addWidget(self.btn_send)

        self.label_send = QLabel(self.widget_send)
        self.label_send.setObjectName(u"label_send")
        self.label_send.setMinimumSize(QSize(0, 0))
        self.label_send.setMaximumSize(QSize(60, 25))
        self.label_send.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_send.setStyleSheet(u"font: 9pt \"Arial\";\n"
"color: rgb(188, 188, 188);\n"
"")

        self.horizontalLayout_9.addWidget(self.label_send)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.widget_send)

        self.tabWidget.addTab(self.tab_AI, "")
        self.tab_params = QWidget()
        self.tab_params.setObjectName(u"tab_params")
        self.tab_params.setStyleSheet(u"")
        self.widget_params = QWidget(self.tab_params)
        self.widget_params.setObjectName(u"widget_params")
        self.widget_params.setGeometry(QRect(30, 30, 301, 471))
        self.verticalLayout_6 = QVBoxLayout(self.widget_params)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.gridLayout_conf = QGridLayout()
        self.gridLayout_conf.setSpacing(0)
        self.gridLayout_conf.setObjectName(u"gridLayout_conf")
        self.label_conf = QLabel(self.widget_params)
        self.label_conf.setObjectName(u"label_conf")

        self.gridLayout_conf.addWidget(self.label_conf, 0, 0, 1, 1)

        self.lineEdit_conf = QLineEdit(self.widget_params)
        self.lineEdit_conf.setObjectName(u"lineEdit_conf")

        self.gridLayout_conf.addWidget(self.lineEdit_conf, 0, 1, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_conf)

        self.gridLayout_nums = QGridLayout()
        self.gridLayout_nums.setSpacing(0)
        self.gridLayout_nums.setObjectName(u"gridLayout_nums")
        self.label_nums = QLabel(self.widget_params)
        self.label_nums.setObjectName(u"label_nums")

        self.gridLayout_nums.addWidget(self.label_nums, 0, 0, 1, 1)

        self.lineEdit_nums = QLineEdit(self.widget_params)
        self.lineEdit_nums.setObjectName(u"lineEdit_nums")

        self.gridLayout_nums.addWidget(self.lineEdit_nums, 0, 1, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_nums)

        self.widget_JSON = QWidget(self.widget_params)
        self.widget_JSON.setObjectName(u"widget_JSON")
        self.verticalLayout_12 = QVBoxLayout(self.widget_JSON)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_JSON = QGridLayout()
        self.gridLayout_JSON.setObjectName(u"gridLayout_JSON")
        self.label_JSON = QLabel(self.widget_JSON)
        self.label_JSON.setObjectName(u"label_JSON")

        self.gridLayout_JSON.addWidget(self.label_JSON, 0, 0, 1, 1)

        self.rb_JSON_y = QRadioButton(self.widget_JSON)
        self.rb_JSON_y.setObjectName(u"rb_JSON_y")

        self.gridLayout_JSON.addWidget(self.rb_JSON_y, 0, 1, 1, 1)

        self.rb_JSON_n = QRadioButton(self.widget_JSON)
        self.rb_JSON_n.setObjectName(u"rb_JSON_n")
        self.rb_JSON_n.setChecked(True)

        self.gridLayout_JSON.addWidget(self.rb_JSON_n, 0, 2, 1, 1)


        self.verticalLayout_12.addLayout(self.gridLayout_JSON)


        self.verticalLayout_6.addWidget(self.widget_JSON)

        self.widget_txt = QWidget(self.widget_params)
        self.widget_txt.setObjectName(u"widget_txt")
        self.verticalLayout_13 = QVBoxLayout(self.widget_txt)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_txt = QGridLayout()
        self.gridLayout_txt.setObjectName(u"gridLayout_txt")
        self.label_txt = QLabel(self.widget_txt)
        self.label_txt.setObjectName(u"label_txt")

        self.gridLayout_txt.addWidget(self.label_txt, 0, 0, 1, 1)

        self.rb_txt_y = QRadioButton(self.widget_txt)
        self.rb_txt_y.setObjectName(u"rb_txt_y")

        self.gridLayout_txt.addWidget(self.rb_txt_y, 0, 1, 1, 1)

        self.rb_txt_n = QRadioButton(self.widget_txt)
        self.rb_txt_n.setObjectName(u"rb_txt_n")
        self.rb_txt_n.setChecked(True)

        self.gridLayout_txt.addWidget(self.rb_txt_n, 0, 2, 1, 1)


        self.verticalLayout_13.addLayout(self.gridLayout_txt)


        self.verticalLayout_6.addWidget(self.widget_txt)

        self.widget_hide = QWidget(self.widget_params)
        self.widget_hide.setObjectName(u"widget_hide")
        self.verticalLayout_14 = QVBoxLayout(self.widget_hide)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_hide = QGridLayout()
        self.gridLayout_hide.setObjectName(u"gridLayout_hide")
        self.label_hidelb = QLabel(self.widget_hide)
        self.label_hidelb.setObjectName(u"label_hidelb")

        self.gridLayout_hide.addWidget(self.label_hidelb, 0, 0, 1, 1)

        self.rb_hidel_y = QRadioButton(self.widget_hide)
        self.rb_hidel_y.setObjectName(u"rb_hidel_y")

        self.gridLayout_hide.addWidget(self.rb_hidel_y, 0, 1, 1, 1)

        self.rb_hidel_n = QRadioButton(self.widget_hide)
        self.rb_hidel_n.setObjectName(u"rb_hidel_n")
        self.rb_hidel_n.setChecked(True)

        self.gridLayout_hide.addWidget(self.rb_hidel_n, 0, 2, 1, 1)


        self.verticalLayout_14.addLayout(self.gridLayout_hide)


        self.verticalLayout_6.addWidget(self.widget_hide)

        self.widget_hidec = QWidget(self.widget_params)
        self.widget_hidec.setObjectName(u"widget_hidec")
        self.verticalLayout_15 = QVBoxLayout(self.widget_hidec)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_hidec = QGridLayout()
        self.gridLayout_hidec.setObjectName(u"gridLayout_hidec")
        self.label_hide_conf = QLabel(self.widget_hidec)
        self.label_hide_conf.setObjectName(u"label_hide_conf")

        self.gridLayout_hidec.addWidget(self.label_hide_conf, 0, 0, 1, 1)

        self.rb_hidec_y = QRadioButton(self.widget_hidec)
        self.rb_hidec_y.setObjectName(u"rb_hidec_y")

        self.gridLayout_hidec.addWidget(self.rb_hidec_y, 0, 1, 1, 1)

        self.rb_hidec_n = QRadioButton(self.widget_hidec)
        self.rb_hidec_n.setObjectName(u"rb_hidec_n")
        self.rb_hidec_n.setChecked(True)

        self.gridLayout_hidec.addWidget(self.rb_hidec_n, 0, 2, 1, 1)


        self.verticalLayout_15.addLayout(self.gridLayout_hidec)


        self.verticalLayout_6.addWidget(self.widget_hidec)

        self.widget_model = QWidget(self.widget_params)
        self.widget_model.setObjectName(u"widget_model")
        self.layoutWidget = QWidget(self.widget_model)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 207, 34))
        self.gridLayout_model = QGridLayout(self.layoutWidget)
        self.gridLayout_model.setSpacing(0)
        self.gridLayout_model.setObjectName(u"gridLayout_model")
        self.gridLayout_model.setContentsMargins(0, 0, 0, 0)
        self.label_model = QLabel(self.layoutWidget)
        self.label_model.setObjectName(u"label_model")
        self.label_model.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_model.addWidget(self.label_model, 0, 0, 1, 1)

        self.comboBox_model = QComboBox(self.layoutWidget)
        self.comboBox_model.setObjectName(u"comboBox_model")

        self.gridLayout_model.addWidget(self.comboBox_model, 0, 1, 1, 1)


        self.verticalLayout_6.addWidget(self.widget_model)

        self.tabWidget.addTab(self.tab_params, "")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.horizontalLayout_11.addWidget(self.main_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_origin.setCurrentIndex(2)
        self.tabWidget_detect.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"\u57fa\u4e8e\n"
"Langchain\u00b7YOLOv8\u7684PCB\u667a\u80fd\n"
"\u7f3a\u9677\u68c0\u6d4b\u7cfb\u7edf", None))
        self.bt_dt_Stage.setText(QCoreApplication.translate("MainWindow", u"\u7f3a\u9677\u68c0\u6d4b", None))
        self.btn_history.setText(QCoreApplication.translate("MainWindow", u"\u5386\u53f2\u8bb0\u5f55", None))
        self.btn_AI.setText(QCoreApplication.translate("MainWindow", u"\u667a\u80fd\u52a9\u624b", None))
        self.btn_params.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8bbe\u7f6e", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa\u7cfb\u7edf", None))
        self.lb_input.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6d41\u9009\u62e9:", None))
        self.input_fileBrowser.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1\U00006d4f\U000089c8", None))
        self.label_camr.setText(QCoreApplication.translate("MainWindow", u"\u6444\u50cf\u5934:", None))
        self.btn_camr.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.label_o.setText(QCoreApplication.translate("MainWindow", u"\u539f\u56fe\u533a", None))
        self.tabWidget_origin.setTabText(self.tabWidget_origin.indexOf(self.pic_o), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget_origin.setTabText(self.tabWidget_origin.indexOf(self.video_o), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidget_origin.setTabText(self.tabWidget_origin.indexOf(self.camr_o), QCoreApplication.translate("MainWindow", u"\u9875", None))
        self.label_d.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u533a", None))
        self.tabWidget_detect.setTabText(self.tabWidget_detect.indexOf(self.pic_d), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget_detect.setTabText(self.tabWidget_detect.indexOf(self.video_d), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidget_detect.setTabText(self.tabWidget_detect.indexOf(self.camr_d), QCoreApplication.translate("MainWindow", u"\u9875", None))
        self.lb_hint.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u793a\u4fe1\u606f: \u6682\u65e0", None))
        self.bt_video_control.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c", None))
        self.bt_save.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.bt_detect.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_detection), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.label_save.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8def\u5f84:", None))
        self.output_fileBrowser.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1\U00006d4f\U000089c8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_history), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.lb_AI_name.setText(QCoreApplication.translate("MainWindow", u"🤖\u667a\u80fdAI\u52a9\u624b", None))
        self.btn_init_model.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u4fe1\u606f", None))
        self.textEdit_question.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u6d88\u606f...", None))
        self.btn_send.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
#if QT_CONFIG(shortcut)
        self.btn_send.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+Return", None))
#endif // QT_CONFIG(shortcut)
        self.label_send.setText(QCoreApplication.translate("MainWindow", u"shift+enter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_AI), QCoreApplication.translate("MainWindow", u"\u9875", None))
        self.label_conf.setText(QCoreApplication.translate("MainWindow", u"\u7f6e\u4fe1\u5ea6:", None))
        self.lineEdit_conf.setText(QCoreApplication.translate("MainWindow", u"0.25", None))
        self.label_nums.setText(QCoreApplication.translate("MainWindow", u"缺陷数量限制:", None))
        self.lineEdit_nums.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.label_JSON.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u4fdd\u5b58JSON\u6587\u4ef6:", None))
        self.rb_JSON_y.setText(QCoreApplication.translate("MainWindow", u"\u662f", None))
        self.rb_JSON_n.setText(QCoreApplication.translate("MainWindow", u"\u5426", None))
        self.label_txt.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u4fdd\u5b58txt\u7ed3\u679c:", None))
        self.rb_txt_y.setText(QCoreApplication.translate("MainWindow", u"\u662f", None))
        self.rb_txt_n.setText(QCoreApplication.translate("MainWindow", u"\u5426", None))
        self.label_hidelb.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u9690\u85cf\u6807\u7b7e:", None))
        self.rb_hidel_y.setText(QCoreApplication.translate("MainWindow", u"\u662f", None))
        self.rb_hidel_n.setText(QCoreApplication.translate("MainWindow", u"\u5426", None))
        self.label_hide_conf.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u9690\u85cf\u7f6e\u4fe1\u5ea6:", None))
        self.rb_hidec_y.setText(QCoreApplication.translate("MainWindow", u"\u662f", None))
        self.rb_hidec_n.setText(QCoreApplication.translate("MainWindow", u"\u5426", None))
        self.label_model.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u9009\u62e9:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_params), QCoreApplication.translate("MainWindow", u"\u9875", None))
    # retranslateUi


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import serial
import serial.tools.list_ports
from datetime import datetime
import threading
import time

M_CurrentPos = [0.0,0.0,0.0]
Machine_Max_UpperLim = [205,190,60]
Machine_Max_LowerLim= [-205,-190,-60]
M_HomePos = [0,0,0]

OnlyFloat = QtGui.QDoubleValidator(
                -9999.0, # bottom
                9999.0, # top
                1, # decimals 
                notation=QtGui.QDoubleValidator.StandardNotation)
M_Pose = [0.00,0.00,0.00]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # config interface
        self.IsMoving = 0
        self.IsAllMoving = 0
        self.AdjustFlag = 0
        self.Move_Flag = 0
        self.M_CurrentPos = [0.0, 0.0, 0.0]
        #--------------# config widget 
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 781)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1021, 741))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.COM_comboBox = QtWidgets.QComboBox(self.tab)
        self.COM_comboBox.setGeometry(QtCore.QRect(150, 40, 73, 22))
        self.COM_comboBox.setObjectName("COM_comboBox")
        self.Baudrate_comboBox = QtWidgets.QComboBox(self.tab)
        self.Baudrate_comboBox.setGeometry(QtCore.QRect(150, 70, 73, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Baudrate_comboBox.setFont(font)
        self.Baudrate_comboBox.setObjectName("Baudrate_comboBox")
        self.Baudrate_comboBox.addItem("")
        self.Baudrate_comboBox.addItem("")
        self.Baudrate_comboBox.addItem("")
        self.Baudrate_comboBox.addItem("")
        self.Baudrate_comboBox.addItem("")
        self.Baudrate_comboBox.addItem("")
        self.Baudrate_comboBox.addItem("")
        self.Baudrate_comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Refresh_pushButton = QtWidgets.QPushButton(self.tab)
        self.Refresh_pushButton.setGeometry(QtCore.QRect(20, 110, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Refresh_pushButton.setFont(font)
        self.Refresh_pushButton.setObjectName("Refresh_pushButton")
        self.Connect_pushButton = QtWidgets.QPushButton(self.tab)
        self.Connect_pushButton.setGeometry(QtCore.QRect(130, 110, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Connect_pushButton.setFont(font)
        self.Connect_pushButton.setObjectName("Connect_pushButton")
        self.Refresh_pushButton.clicked.connect(self.refresh_ports)
        self.Connect_pushButton.clicked.connect(self.connect_or_disconnect)
        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setGeometry(QtCore.QRect(5, 5, 241, 150))
        self.tableView.setObjectName("tableView")
        self.tableView_2 = QtWidgets.QTableView(self.tab)
        self.tableView_2.setGeometry(QtCore.QRect(250, 5, 761, 426))
        self.tableView_2.setObjectName("tableView_2")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(280, 240, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.YPos_pushButton = QtWidgets.QPushButton(self.tab)
        self.YPos_pushButton.setGeometry(QtCore.QRect(460, 240, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.YPos_pushButton.setFont(font)
        self.YPos_pushButton.setObjectName("YPos_pushButton")
        self.YNeg_pushButton = QtWidgets.QPushButton(self.tab)
        self.YNeg_pushButton.setGeometry(QtCore.QRect(460, 360, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.YNeg_pushButton.setFont(font)
        self.YNeg_pushButton.setObjectName("YNeg_pushButton")
        self.XNeg_pushButton = QtWidgets.QPushButton(self.tab)
        self.XNeg_pushButton.setGeometry(QtCore.QRect(380, 300, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.XNeg_pushButton.setFont(font)
        self.XNeg_pushButton.setObjectName("XNeg_pushButton")
        self.XPos_pushButton = QtWidgets.QPushButton(self.tab)
        self.XPos_pushButton.setGeometry(QtCore.QRect(540, 300, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.XPos_pushButton.setFont(font)
        self.XPos_pushButton.setObjectName("XPos_pushButton")
        self.ZPos_pushButton = QtWidgets.QPushButton(self.tab)
        self.ZPos_pushButton.setGeometry(QtCore.QRect(620, 240, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ZPos_pushButton.setFont(font)
        self.ZPos_pushButton.setObjectName("ZPos_pushButton")
        self.ZNeg_pushButton = QtWidgets.QPushButton(self.tab)
        self.ZNeg_pushButton.setGeometry(QtCore.QRect(620, 360, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ZNeg_pushButton.setFont(font)
        self.ZNeg_pushButton.setObjectName("ZNeg_pushButton")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(270, 280, 101, 141))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.disable_move_buttons()
        self.Hundred_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.Hundred_radioButton.setGeometry(QtCore.QRect(10, 20, 51, 20))
        self.Hundred_radioButton.setObjectName("Hundred_radioButton")
        self.Ten_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.Ten_radioButton.setGeometry(QtCore.QRect(10, 50, 51, 20))
        self.Ten_radioButton.setObjectName("Ten_radioButton")
        self.One_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.One_radioButton.setGeometry(QtCore.QRect(10, 80, 51, 20))
        self.One_radioButton.setObjectName("One_radioButton")
        self.DotOne_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.DotOne_radioButton.setGeometry(QtCore.QRect(10, 110, 51, 20))
        self.DotOne_radioButton.setObjectName("DotOne_radioButton")
        self.Hundred_radioButton.toggled.connect(self.check_radio_buttons)
        self.Ten_radioButton.toggled.connect(self.check_radio_buttons)
        self.One_radioButton.toggled.connect(self.check_radio_buttons)
        self.DotOne_radioButton.toggled.connect(self.check_radio_buttons)
        self.Hundred_radioButton.setEnabled(False)
        self.Ten_radioButton.setEnabled(False)
        self.One_radioButton.setEnabled(False)
        self.DotOne_radioButton.setEnabled(False)               
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(500, 20, 20, 201))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(260, 10, 55, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(260, 40, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(260, 90, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(260, 140, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.X_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.X_lineEdit.setGeometry(QtCore.QRect(300, 50, 113, 22))
        self.X_lineEdit.setObjectName("X_lineEdit")
        self.X_lineEdit.setValidator(OnlyFloat)
        self.X_lineEdit.setText(f"{M_Pose[0]:.2f}")
        self.Y_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.Y_lineEdit.setGeometry(QtCore.QRect(300, 100, 113, 22))
        self.Y_lineEdit.setObjectName("Y_lineEdit")
        self.Y_lineEdit.setValidator(OnlyFloat)
        self.Y_lineEdit.setText(f"{M_Pose[1]:.2f}")
        self.Z_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.Z_lineEdit.setGeometry(QtCore.QRect(300, 150, 113, 22))
        self.Z_lineEdit.setObjectName("Z_lineEdit")
        self.Z_lineEdit.setValidator(OnlyFloat)
        self.Z_lineEdit.setText(f"{M_Pose[2]:.2f}")
        self.XHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.XHome_pushButton.setGeometry(QtCore.QRect(430, 45, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.XHome_pushButton.setFont(font)
        self.XHome_pushButton.setObjectName("XHome_pushButton")
        self.YHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.YHome_pushButton.setGeometry(QtCore.QRect(430, 95, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.YHome_pushButton.setFont(font)
        self.YHome_pushButton.setObjectName("YHome_pushButton")
        self.ZHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.ZHome_pushButton.setGeometry(QtCore.QRect(430, 145, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.ZHome_pushButton.setFont(font)
        self.ZHome_pushButton.setObjectName("ZHome_pushButton")
        self.AllHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.AllHome_pushButton.setGeometry(QtCore.QRect(430, 190, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.AllHome_pushButton.setFont(font)
        self.AllHome_pushButton.setObjectName("AllHome_pushButton")
        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setGeometry(QtCore.QRect(260, 220, 711, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(520, 30, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.Gcode_textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.Gcode_textBrowser.setGeometry(QtCore.QRect(520, 60, 291, 31))
        self.Gcode_textBrowser.setObjectName("Gcode_textBrowser")
        self.Load_pushButton = QtWidgets.QPushButton(self.tab)
        self.Load_pushButton.setGeometry(QtCore.QRect(520, 110, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Load_pushButton.setFont(font)
        self.Load_pushButton.setObjectName("Load_pushButton")
        self.Delete_pushButton = QtWidgets.QPushButton(self.tab)
        self.Delete_pushButton.setGeometry(QtCore.QRect(620, 110, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Delete_pushButton.setFont(font)
        self.Delete_pushButton.setObjectName("Delete_pushButton")
        self.Browse_pushButton = QtWidgets.QPushButton(self.tab)
        self.Browse_pushButton.setGeometry(QtCore.QRect(720, 110, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Browse_pushButton.setFont(font)
        self.Browse_pushButton.setObjectName("Browse_pushButton")
        self.Browse_pushButton.clicked.connect(self.browse_file)
        self.tableView_4 = QtWidgets.QTableView(self.tab)
        self.tableView_4.setGeometry(QtCore.QRect(5, 160, 241, 271))
        self.tableView_4.setObjectName("tableView_4")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(10, 170, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(520, 150, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.ManualCommand_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.ManualCommand_lineEdit.setGeometry(QtCore.QRect(520, 180, 191, 31))
        self.ManualCommand_lineEdit.setObjectName("ManualCommand_lineEdit")
        self.Send_pushButton = QtWidgets.QPushButton(self.tab)
        self.Send_pushButton.setGeometry(QtCore.QRect(720, 180, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Send_pushButton.setFont(font)
        self.Send_pushButton.setObjectName("Send_pushButton")
        self.XCalibrate_pushButton = QtWidgets.QPushButton(self.tab)
        self.XCalibrate_pushButton.setGeometry(QtCore.QRect(20, 190, 93, 28))
        self.XCalibrate_pushButton.setObjectName("XCalibrate_pushButton")
        self.YCalibrate_pushButton = QtWidgets.QPushButton(self.tab)
        self.YCalibrate_pushButton.setGeometry(QtCore.QRect(20, 230, 93, 28))
        self.YCalibrate_pushButton.setObjectName("YCalibrate_pushButton")
        self.ZCalibrate_pushButton = QtWidgets.QPushButton(self.tab)
        self.ZCalibrate_pushButton.setGeometry(QtCore.QRect(20, 270, 93, 28))
        self.ZCalibrate_pushButton.setObjectName("ZCalibrate_pushButton")
        self.Move_pushButton = QtWidgets.QPushButton(self.tab)
        self.Move_pushButton.setGeometry(QtCore.QRect(343, 190, 71, 31))
        self.Move_pushButton.clicked.connect(self.move_command)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Move_pushButton.setFont(font)
        self.Move_pushButton.setObjectName("Move_pushButton")
        self.XEnabled_pushButton = QtWidgets.QPushButton(self.tab)
        self.XEnabled_pushButton.setGeometry(QtCore.QRect(130, 190, 93, 28))
        self.XEnabled_pushButton.setObjectName("XEnabled_pushButton")
        self.YEnabled_pushButton = QtWidgets.QPushButton(self.tab)
        self.YEnabled_pushButton.setGeometry(QtCore.QRect(130, 230, 93, 28))
        self.YEnabled_pushButton.setObjectName("YEnabled_pushButton")
        self.ZEnabled_pushButton = QtWidgets.QPushButton(self.tab)
        self.ZEnabled_pushButton.setGeometry(QtCore.QRect(130, 270, 93, 28))
        self.ZEnabled_pushButton.setObjectName("ZEnabled_pushButton")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_2.setGeometry(QtCore.QRect(5, 440, 581, 261))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.AllCalibrate_pushButton = QtWidgets.QPushButton(self.tab)
        self.AllCalibrate_pushButton.setGeometry(QtCore.QRect(20, 310, 93, 28))
        self.AllCalibrate_pushButton.setObjectName("AllCalibrate_pushButton")
        self.AllEnabled_pushButton = QtWidgets.QPushButton(self.tab)
        self.AllEnabled_pushButton.setGeometry(QtCore.QRect(130, 310, 93, 28))
        self.AllEnabled_pushButton.setObjectName("AllEnabled_pushButton")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(10, 450, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.Status_textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.Status_textBrowser.setGeometry(QtCore.QRect(14, 480, 566, 211))
        self.Status_textBrowser.setObjectName("Status_textBrowser")
        self.ClearMessage_pushButton = QtWidgets.QPushButton(self.tab)
        self.ClearMessage_pushButton.setGeometry(QtCore.QRect(460, 450, 121, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.ClearMessage_pushButton.setFont(font)
        self.ClearMessage_pushButton.setObjectName("ClearMessage_pushButton")
        self.ClearMessage_pushButton.clicked.connect(self.clear_messages)
        self.listView = QtWidgets.QListView(self.tab)
        self.listView.setGeometry(QtCore.QRect(590, 440, 421, 261))
        self.listView.setObjectName("listView")
        self.Gcode_tableWidget = QtWidgets.QTableWidget(self.tab)
        self.Gcode_tableWidget.setGeometry(QtCore.QRect(600, 450, 401, 241))
        self.Gcode_tableWidget.setObjectName("Gcode_tableWidget")
        self.Gcode_tableWidget.setColumnCount(3)
        self.Gcode_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        item.setFont(font)
        self.Gcode_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Gcode_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Gcode_tableWidget.setHorizontalHeaderItem(2, item)
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(720, 10, 191, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(720, 35, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.photo = QtWidgets.QLabel(self.tab)
        self.photo.setGeometry(QtCore.QRect(920, 10, 61, 61))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("logoIU.png"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(740, 240, 51, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.line_3 = QtWidgets.QFrame(self.tab)
        self.line_3.setGeometry(QtCore.QRect(700, 240, 20, 181))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(720, 278, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.XOffset_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.tab)
        self.XOffset_doubleSpinBox.setGeometry(QtCore.QRect(790, 276, 62, 22))
        self.XOffset_doubleSpinBox.setMinimum(-1000.0)
        self.XOffset_doubleSpinBox.setMaximum(1000.0)
        self.XOffset_doubleSpinBox.setSingleStep(0.1)
        self.XOffset_doubleSpinBox.setObjectName("XOffset_doubleSpinBox")
        self.label_17 = QtWidgets.QLabel(self.tab)
        self.label_17.setGeometry(QtCore.QRect(720, 320, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.YOffset_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.tab)
        self.YOffset_doubleSpinBox.setGeometry(QtCore.QRect(790, 318, 62, 22))
        self.YOffset_doubleSpinBox.setMinimum(-1000.0)
        self.YOffset_doubleSpinBox.setMaximum(1000.0)
        self.YOffset_doubleSpinBox.setSingleStep(0.1)
        self.YOffset_doubleSpinBox.setObjectName("YOffset_doubleSpinBox")
        self.label_18 = QtWidgets.QLabel(self.tab)
        self.label_18.setGeometry(QtCore.QRect(720, 360, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.ZOffset_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.tab)
        self.ZOffset_doubleSpinBox.setGeometry(QtCore.QRect(790, 358, 62, 22))
        self.ZOffset_doubleSpinBox.setMinimum(-1000.0)
        self.ZOffset_doubleSpinBox.setMaximum(1000.0)
        self.ZOffset_doubleSpinBox.setSingleStep(0.1)
        self.ZOffset_doubleSpinBox.setObjectName("ZOffset_doubleSpinBox")
        self.label_19 = QtWidgets.QLabel(self.tab)
        self.label_19.setGeometry(QtCore.QRect(870, 240, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.Offset_ComboBox = QtWidgets.QComboBox(self.tab)
        self.Offset_ComboBox.setGeometry(QtCore.QRect(900, 276, 73, 22))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Offset_ComboBox.setFont(font)
        self.Offset_ComboBox.setObjectName("Offset_ComboBox")
        self.Save_pushButton = QtWidgets.QPushButton(self.tab)
        self.Save_pushButton.setGeometry(QtCore.QRect(900, 310, 73, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Save_pushButton.setFont(font)
        self.Save_pushButton.setObjectName("Save_pushButton")
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setGeometry(QtCore.QRect(20, 340, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.tab)
        self.label_21.setGeometry(QtCore.QRect(20, 380, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.Speed_horizontalSlider = QtWidgets.QSlider(self.tab)
        self.Speed_horizontalSlider.setGeometry(QtCore.QRect(20, 360, 140, 22))
        self.Speed_horizontalSlider.setMinimum(1)
        self.Speed_horizontalSlider.setMaximum(5)
        self.Speed_horizontalSlider.setSingleStep(1)
        self.Speed_horizontalSlider.setPageStep(5)
        self.Speed_horizontalSlider.setProperty("value", 1)
        self.Speed_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.Speed_horizontalSlider.setObjectName("Speed_horizontalSlider")
        self.Speed_horizontalSlider.sliderReleased.connect(self.update_speed_label)
        self.Speed_horizontalSlider.sliderReleased.connect(self.update_speed_label1)
        self.Acceleration_horizontalSlider = QtWidgets.QSlider(self.tab)
        self.Acceleration_horizontalSlider.setGeometry(QtCore.QRect(20, 400, 140, 22))
        self.Acceleration_horizontalSlider.setMinimum(1)
        self.Acceleration_horizontalSlider.setMaximum(5)
        self.Acceleration_horizontalSlider.setPageStep(1)
        self.Acceleration_horizontalSlider.setProperty("value", 1)
        self.Acceleration_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.Acceleration_horizontalSlider.setObjectName("Acceleration_horizontalSlider")
        self.Acceleration_horizontalSlider.sliderReleased.connect(self.update_accel_label)
        self.Acceleration_horizontalSlider.sliderReleased.connect(self.update_accel_label1)
        self.label_22 = QtWidgets.QLabel(self.tab)
        self.label_22.setGeometry(QtCore.QRect(170, 360, 70, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.tab)
        self.label_23.setGeometry(QtCore.QRect(170, 400, 70, 20))
        self.label_23.setObjectName("label_23")
        self.Hold_pushButton = QtWidgets.QPushButton(self.tab)
        self.Hold_pushButton.setGeometry(QtCore.QRect(260, 190, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Hold_pushButton.setFont(font)
        self.Hold_pushButton.setObjectName("Hold_pushButton")
        self.Start_pushButton = QtWidgets.QPushButton(self.tab)
        self.Start_pushButton.setGeometry(QtCore.QRect(820, 59,71, 41))
        self.Start_pushButton.setObjectName("Start_pushButton")
        self.tableView.raise_()
        self.COM_comboBox.raise_()
        self.Baudrate_comboBox.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.Refresh_pushButton.raise_()
        self.Connect_pushButton.raise_()
        self.tableView_2.raise_()
        self.label_4.raise_()
        self.YPos_pushButton.raise_()
        self.YNeg_pushButton.raise_()
        self.XNeg_pushButton.raise_()
        self.XPos_pushButton.raise_()
        self.ZPos_pushButton.raise_()
        self.ZNeg_pushButton.raise_()
        self.groupBox.raise_()
        self.line.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.X_lineEdit.raise_()
        self.Y_lineEdit.raise_()
        self.Z_lineEdit.raise_()
        self.XHome_pushButton.raise_()
        self.YHome_pushButton.raise_()
        self.ZHome_pushButton.raise_()
        self.AllHome_pushButton.raise_()
        self.line_2.raise_()
        self.label_10.raise_()
        self.Gcode_textBrowser.raise_()
        self.Load_pushButton.raise_()
        self.Delete_pushButton.raise_()
        self.Browse_pushButton.raise_()
        self.tableView_4.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.ManualCommand_lineEdit.raise_()
        self.Send_pushButton.raise_()
        self.XCalibrate_pushButton.raise_()
        self.YCalibrate_pushButton.raise_()
        self.ZCalibrate_pushButton.raise_()
        self.Move_pushButton.raise_()
        self.XEnabled_pushButton.raise_()
        self.YEnabled_pushButton.raise_()
        self.ZEnabled_pushButton.raise_()
        self.textBrowser_2.raise_()
        self.AllCalibrate_pushButton.raise_()
        self.AllEnabled_pushButton.raise_()
        self.label_9.raise_()
        self.Status_textBrowser.raise_()
        self.ClearMessage_pushButton.raise_()
        self.listView.raise_()
        self.Gcode_tableWidget.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.photo.raise_()
        self.label_15.raise_()
        self.line_3.raise_()
        self.label_16.raise_()
        self.XOffset_doubleSpinBox.raise_()
        self.label_17.raise_()
        self.YOffset_doubleSpinBox.raise_()
        self.label_18.raise_()
        self.ZOffset_doubleSpinBox.raise_()
        self.label_19.raise_()
        self.Offset_ComboBox.raise_()
        self.Save_pushButton.raise_()
        self.label_20.raise_()
        self.label_21.raise_()
        self.Speed_horizontalSlider.raise_()
        self.Acceleration_horizontalSlider.raise_()
        self.label_22.raise_()
        self.label_23.raise_()
        self.Hold_pushButton.raise_()
        self.Start_pushButton.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 26))
        self.menubar.setObjectName("menubar")
        self.menuFILE = QtWidgets.QMenu(self.menubar)
        self.menuFILE.setObjectName("menuFILE")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.exit_application)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuFILE.addAction(self.actionExit)
        self.menuTools.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFILE.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CNC Control V1"))
        self.Baudrate_comboBox.setItemText(0, _translate("MainWindow", "9600"))
        self.Baudrate_comboBox.setItemText(1, _translate("MainWindow", "14400"))
        self.Baudrate_comboBox.setItemText(2, _translate("MainWindow", "19200"))
        self.Baudrate_comboBox.setItemText(3, _translate("MainWindow", "28800"))
        self.Baudrate_comboBox.setItemText(4, _translate("MainWindow", "31250"))
        self.Baudrate_comboBox.setItemText(5, _translate("MainWindow", "38400"))
        self.Baudrate_comboBox.setItemText(6, _translate("MainWindow", "57600"))
        self.Baudrate_comboBox.setItemText(7, _translate("MainWindow", "115200"))
        self.label.setText(_translate("MainWindow", "Serial Configuration"))
        self.label_2.setText(_translate("MainWindow", "COM:"))
        self.label_3.setText(_translate("MainWindow", "Baudrate:"))
        self.Refresh_pushButton.setText(_translate("MainWindow", "Refresh"))
        self.Connect_pushButton.setText(_translate("MainWindow", "Connect"))
        self.label_4.setText(_translate("MainWindow", "Jogging"))
        self.YPos_pushButton.setText(_translate("MainWindow", "Y +"))
        self.YNeg_pushButton.setText(_translate("MainWindow", "Y -"))
        self.XNeg_pushButton.setText(_translate("MainWindow", "X -"))
        self.XPos_pushButton.setText(_translate("MainWindow", "X -"))
        self.ZPos_pushButton.setText(_translate("MainWindow", "Z +"))
        self.ZNeg_pushButton.setText(_translate("MainWindow", "Z -"))
        self.groupBox.setTitle(_translate("MainWindow", "Distance"))
        self.Hundred_radioButton.setText(_translate("MainWindow", "100"))
        self.Ten_radioButton.setText(_translate("MainWindow", "10"))
        self.One_radioButton.setText(_translate("MainWindow", "1"))
        self.DotOne_radioButton.setText(_translate("MainWindow", "0.1"))
        self.label_5.setText(_translate("MainWindow", "Work"))
        self.label_6.setText(_translate("MainWindow", "X"))
        self.label_7.setText(_translate("MainWindow", "Y"))
        self.label_8.setText(_translate("MainWindow", "Z"))
        self.X_lineEdit.setText(_translate("MainWindow", "0.0"))
        self.Y_lineEdit.setText(_translate("MainWindow", "0.0"))
        self.Z_lineEdit.setText(_translate("MainWindow", "0.0"))
        self.XHome_pushButton.setText(_translate("MainWindow", "Set 0"))
        self.XHome_pushButton.clicked.connect(self.X_Home)
        self.YHome_pushButton.setText(_translate("MainWindow", "Set 0"))
        self.YHome_pushButton.clicked.connect(self.Y_Home)
        self.ZHome_pushButton.setText(_translate("MainWindow", "Set 0"))
        self.ZHome_pushButton.clicked.connect(self.Z_Home)
        self.AllHome_pushButton.setText(_translate("MainWindow", "Home All"))
        self.AllHome_pushButton.clicked.connect(self.Home_All)
        self.label_10.setText(_translate("MainWindow", "G-Code"))
        self.Load_pushButton.setText(_translate("MainWindow", "Load"))
        self.Delete_pushButton.setText(_translate("MainWindow", "Delete"))
        self.Browse_pushButton.setText(_translate("MainWindow", "Browse"))
        self.label_11.setText(_translate("MainWindow", "Basic control"))
        self.label_12.setText(_translate("MainWindow", "Manual Command"))
        self.Send_pushButton.setText(_translate("MainWindow", "Send"))
        self.XCalibrate_pushButton.setText(_translate("MainWindow", "X Calibrate"))
        self.YCalibrate_pushButton.setText(_translate("MainWindow", "Y Calibrate"))
        self.ZCalibrate_pushButton.setText(_translate("MainWindow", "Z Calibrate"))
        self.Move_pushButton.setText(_translate("MainWindow", "Move"))
        self.XEnabled_pushButton.setText(_translate("MainWindow", "X Enabled"))
        self.YEnabled_pushButton.setText(_translate("MainWindow", "Y Enabled"))
        self.ZEnabled_pushButton.setText(_translate("MainWindow", "Z Enabled"))
        self.AllCalibrate_pushButton.setText(_translate("MainWindow", "Calibrate All"))
        self.AllEnabled_pushButton.setText(_translate("MainWindow", "Enabled All"))
        self.label_9.setText(_translate("MainWindow", "Status"))
        self.ClearMessage_pushButton.setText(_translate("MainWindow", "Clear Message"))
        item = self.Gcode_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Status"))
        item = self.Gcode_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Line"))
        item = self.Gcode_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "G code"))
        self.label_13.setText(_translate("MainWindow", "By Nguyen Hoang Khang "))
        self.label_14.setText(_translate("MainWindow", "EEACIU19015 - HCMIU"))
        self.label_15.setText(_translate("MainWindow", "Offset"))
        self.label_16.setText(_translate("MainWindow", "X offset:"))
        self.label_17.setText(_translate("MainWindow", "Y offset:"))
        self.label_18.setText(_translate("MainWindow", "Z offset:"))
        self.label_19.setText(_translate("MainWindow", "Offset position"))
        self.Save_pushButton.setText(_translate("MainWindow", "Save"))
        self.label_20.setText(_translate("MainWindow", "Speed:"))
        self.label_21.setText(_translate("MainWindow", "Acceleration:"))
        self.label_22.setText(_translate("MainWindow", "100, 100, 50"))
        self.label_23.setText(_translate("MainWindow", "200, 200"))
        self.Hold_pushButton.setText(_translate("MainWindow", "Hold"))
        self.Start_pushButton.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Interface"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "View"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Settings"))
        self.menuFILE.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))

    def exit_application(self):
        self.close()
        
    def detect_serial_port(self, arduino_port):
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        return arduino_port in available_ports

    def connect_or_disconnect(self):
        arduino_port = str(self.COM_comboBox.currentText())
        baudrate = int(self.Baudrate_comboBox.currentText())

        current_time = datetime.now().strftime('%H:%M:%S')
        time_message = f"[{current_time}] "

        if self.Connect_pushButton.text() == "Connect":
            if  self.detect_serial_port(arduino_port):
                self.Baudrate_comboBox.setEnabled(False)
                self.COM_comboBox.setEnabled(False)
                self.Hundred_radioButton.setEnabled(True)
                self.Ten_radioButton.setEnabled(True)
                self.One_radioButton.setEnabled(True)
                self.DotOne_radioButton.setEnabled(True)
                try:
                    self.ser = serial.Serial(arduino_port, baudrate)
                    self.Connect_pushButton.setText("Disconnect")
                    self.Status_textBrowser.append(f"{time_message}Connected to Arduino on {arduino_port} with baudrate {baudrate}")
                except serial.SerialException as e:
                    self.Status_textBrowser.append(f"{time_message}Error: {e}")
            else:
                self.Status_textBrowser.append(f"{time_message}Arduino not found on {arduino_port}")
        else:
            if hasattr(self, 'ser') and self.ser.is_open:
                self.ser.close()
                self.Connect_pushButton.setText("Connect")
                self.Status_textBrowser.append(f"{time_message}Disconnected from Arduino")
                self.Baudrate_comboBox.setEnabled(True)
                self.COM_comboBox.setEnabled(True)
                self.Hundred_radioButton.setEnabled(False)
                self.Ten_radioButton.setEnabled(False)
                self.One_radioButton.setEnabled(False)
                self.DotOne_radioButton.setEnabled(False)
                self.disable_move_buttons()

    def refresh_ports(self):
        # Clear and repopulate COM ports
        self.COM_comboBox.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.COM_comboBox.addItem(port.device)
    
    def clear_messages(self):
        # Clear the content of the SystemM_textBrowser
        self.Status_textBrowser.clear()
        current_time = datetime.now().strftime('%H:%M:%S')  # Get the current time
        self.Status_textBrowser.append(f"[{current_time}] Messages cleared")
    
    def browse_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Browse G-code file", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            print(f"Selected file: {fileName}")
            self.Status_textBrowser.append(f"Selected file: {fileName}")
        else:
            print("File selection canceled")
            self.Status_textBrowser.append("File selection canceled")     
    def X_Home(self):
        x_coord_v = 0.0 
        y_coord_v = M_CurrentPos[1]
        z_coord_v = M_CurrentPos[2]

        x_ToMove = x_coord_v - M_CurrentPos[0]
        y_ToMove = y_coord_v - M_CurrentPos[1]
        z_ToMove = z_coord_v - M_CurrentPos[2]

        M_CurrentPos[0] = x_coord_v
        M_CurrentPos[1] = y_coord_v
        M_CurrentPos[2] = z_coord_v

        # Generate the G-code command
        gcode_command_parts = []
        gcode_command_parts.append(f"X{x_ToMove}")
        gcode_command_parts.append(f"Y{y_ToMove}")
        gcode_command_parts.append(f"Z{z_ToMove}")
        gcode_command = "G0 " + " ".join(gcode_command_parts)
        gcode_send = "G0X{:0=+06.1f}Y{:0=+06.1f}Z{:0=+06.1f}".format(float(x_ToMove), float(y_ToMove), float(z_ToMove))
        # Send the G-code to Arduino 
        self.send_to_arduino(gcode_send)
        self.display_gcode(gcode_command)
        # set line dit cho current pos
        self.X_lineEdit.setText(str(M_CurrentPos[0]))
        self.Y_lineEdit.setText(str(M_CurrentPos[1]))
        self.Z_lineEdit.setText(str(M_CurrentPos[2]))
    
    def Y_Home(self):
        x_coord_v = M_CurrentPos[0]
        y_coord_v = 0.0
        z_coord_v = M_CurrentPos[2]

        x_ToMove = x_coord_v - M_CurrentPos[0]
        y_ToMove = y_coord_v - M_CurrentPos[1]
        z_ToMove = z_coord_v - M_CurrentPos[2]

        M_CurrentPos[0] = x_coord_v
        M_CurrentPos[1] = y_coord_v
        M_CurrentPos[2] = z_coord_v

        # Generate the G-code command
        gcode_command_parts = []
        gcode_command_parts.append(f"X{x_ToMove}")
        gcode_command_parts.append(f"Y{y_ToMove}")
        gcode_command_parts.append(f"Z{z_ToMove}")
        gcode_command = "G0 " + " ".join(gcode_command_parts)
        gcode_send = "G0X{:0=+06.1f}Y{:0=+06.1f}Z{:0=+06.1f}".format(float(x_ToMove), float(y_ToMove), float(z_ToMove))
        # Send the G-code to Arduino 
        self.send_to_arduino(gcode_send)
        self.display_gcode(gcode_command)
        # set line dit cho current pos
        self.X_lineEdit.setText(str(M_CurrentPos[0]))
        self.Y_lineEdit.setText(str(M_CurrentPos[1]))
        self.Z_lineEdit.setText(str(M_CurrentPos[2]))

    def Z_Home(self):
        x_coord_v = M_CurrentPos[0]
        y_coord_v = M_CurrentPos[1]
        z_coord_v = 0.0

        x_ToMove = x_coord_v - M_CurrentPos[0]
        y_ToMove = y_coord_v - M_CurrentPos[1]
        z_ToMove = z_coord_v - M_CurrentPos[2]

        M_CurrentPos[0] = x_coord_v
        M_CurrentPos[1] = y_coord_v
        M_CurrentPos[2] = z_coord_v

        # Generate the G-code command
        gcode_command_parts = []
        gcode_command_parts.append(f"X{x_ToMove}")
        gcode_command_parts.append(f"Y{y_ToMove}")
        gcode_command_parts.append(f"Z{z_ToMove}")
        gcode_command = "G0 " + " ".join(gcode_command_parts)
        gcode_send = "G0X{:0=+06.1f}Y{:0=+06.1f}Z{:0=+06.1f}".format(float(x_ToMove), float(y_ToMove), float(z_ToMove))
        # Send the G-code to Arduino 
        self.send_to_arduino(gcode_send)
        self.display_gcode(gcode_command)
        # set line dit cho current pos
        self.X_lineEdit.setText(str(M_CurrentPos[0]))
        self.Y_lineEdit.setText(str(M_CurrentPos[1]))
        self.Z_lineEdit.setText(str(M_CurrentPos[2]))

    def Home_All(self):
        # Get the values from the lineEdits
        x_coord_v = 0.0 
        y_coord_v = 0.0 
        z_coord_v = 0.0 

        x_ToMove = x_coord_v - M_CurrentPos[0]
        y_ToMove = y_coord_v - float(M_CurrentPos[1])
        z_ToMove = z_coord_v - float(M_CurrentPos[2])

        M_CurrentPos[0] = x_coord_v
        M_CurrentPos[1] = y_coord_v
        M_CurrentPos[2] = z_coord_v

        # Generate the G-code command
        gcode_command_parts = []
        gcode_command_parts.append(f"X{x_ToMove}")
        gcode_command_parts.append(f"Y{y_ToMove}")
        gcode_command_parts.append(f"Z{z_ToMove}")
        gcode_command = "G0 " + " ".join(gcode_command_parts)
        gcode_send = "G0X{:0=+06.1f}Y{:0=+06.1f}Z{:0=+06.1f}".format(float(x_ToMove), float(y_ToMove), float(z_ToMove))
        # Send the G-code to Arduino 
        self.send_to_arduino(gcode_send)
        self.display_gcode(gcode_command)
        # set line dit cho current pos
        self.X_lineEdit.setText(str(M_CurrentPos[0]))
        self.Y_lineEdit.setText(str(M_CurrentPos[1]))
        self.Z_lineEdit.setText(str(M_CurrentPos[2]))

    def check_available(self):
        if self.Connect_pushButton.text() == "Disconnect" and self.IsMoving == 1:
            data = self.read_from_serial_port()
            if data is not None and data.strip() == 'Done':  # Check if 'Done' message is received
                self.Enable_Function()  # Enable all functions
                self.IsMoving = 0

    def move_command(self):
            # Get the values from the lineEdits
            if not self.X_lineEdit.text():
                x_coord_v = M_CurrentPos[0]
            else:
                x_coord_v = float(self.X_lineEdit.text())

            if not self.Y_lineEdit.text():
                y_coord_v = M_CurrentPos[0]
            else:
                y_coord_v = float(self.Y_lineEdit.text())

            if not self.Z_lineEdit.text():
                z_coord_v = M_CurrentPos[0]
            else:
                z_coord_v = float(self.Z_lineEdit.text())
        
            if  x_coord_v > Machine_Max_UpperLim[0]:
                x_coord_v = Machine_Max_UpperLim[0]

            if  y_coord_v > Machine_Max_UpperLim[1]:
                y_coord_v = Machine_Max_UpperLim[1]

            if  z_coord_v > Machine_Max_UpperLim[2]:
                z_coord_v = Machine_Max_UpperLim[2]

            if  x_coord_v < Machine_Max_LowerLim[0]:
                x_coord_v = Machine_Max_LowerLim[0]

            if  y_coord_v < Machine_Max_LowerLim[1]:
                y_coord_v = Machine_Max_LowerLim[1]
            
            if  z_coord_v < Machine_Max_LowerLim[2]:
                z_coord_v = Machine_Max_LowerLim[2]

            x_ToMove = x_coord_v - float(M_CurrentPos[0])
            y_ToMove = y_coord_v - float(M_CurrentPos[1])
            z_ToMove = z_coord_v - float(M_CurrentPos[2])

            M_CurrentPos[0] = x_coord_v
            M_CurrentPos[1] = y_coord_v
            M_CurrentPos[2] = z_coord_v

            # Generate the G-code command
            gcode_command_parts = []
            gcode_command_parts.append(f"X{x_ToMove}")
            gcode_command_parts.append(f"Y{y_ToMove}")
            gcode_command_parts.append(f"Z{z_ToMove}")
            gcode_command = "G0 " + " ".join(gcode_command_parts)
            gcode_send = "G0X{:0=+06.1f}Y{:0=+06.1f}Z{:0=+06.1f}".format(float(x_ToMove), float(y_ToMove), float(z_ToMove))

            # Send the G-code to Arduino
            self.send_to_arduino(gcode_send)
            self.display_gcode(gcode_command)
            # set linerdit cho current pos
            self.X_lineEdit.setText(str(M_CurrentPos[0]))
            self.Y_lineEdit.setText(str(M_CurrentPos[1]))
            self.Z_lineEdit.setText(str(M_CurrentPos[2]))

            

    def send_to_arduino(self, gcode_send):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.write((gcode_send + '\n').encode('ascii'))  # Send the command to Arduino using ASCII encoding
            print(gcode_send)

    def display_gcode(self, gcode_command):
        if hasattr(self, 'ser') and self.ser.is_open:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Sent: {gcode_command}")
            except Exception as e:
                self.Status_textBrowser.append(f"Error sending command: {e}")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def check_radio_buttons(self):
        if hasattr(self, 'ser') and self.ser.is_open:
                
            if      self.Hundred_radioButton.isChecked():
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Distance set at 100 mm")
                    self.Hundred_movement()
                    self.enable_move_buttons()
            elif    self.Ten_radioButton.isChecked():
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Distance set at 10 mm")
                    self.Ten_movement()
                    self.enable_move_buttons()
            elif    self.One_radioButton.isChecked():
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Distance set at 1 mm")
                    self.One_movement()
                    self.enable_move_buttons()
            elif    self.DotOne_radioButton.isChecked():
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Distance set at 0.1 mm")
                    self.DotOne_movement()
                    self.enable_move_buttons()
            else:
                    self.disable_move_buttons()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def Hundred_movement(self):
        self.XPos_pushButton.clicked.connect(lambda: self.move_axis('X', 100))
        self.XNeg_pushButton.clicked.connect(lambda: self.move_axis('X', -100))
        self.YPos_pushButton.clicked.connect(lambda: self.move_axis('Y', 100))
        self.YNeg_pushButton.clicked.connect(lambda: self.move_axis('Y', -100))
        self.ZPos_pushButton.clicked.connect(lambda: self.move_axis('Z', 100))
        self.ZNeg_pushButton.clicked.connect(lambda: self.move_axis('Z', -100))
    
    def Ten_movement(self):
        self.XPos_pushButton.clicked.connect(lambda: self.move_axis('X', 10))
        self.XNeg_pushButton.clicked.connect(lambda: self.move_axis('X', -10))
        self.YPos_pushButton.clicked.connect(lambda: self.move_axis('Y', 10))
        self.YNeg_pushButton.clicked.connect(lambda: self.move_axis('Y', -10))
        self.ZPos_pushButton.clicked.connect(lambda: self.move_axis('Z', 10))
        self.ZNeg_pushButton.clicked.connect(lambda: self.move_axis('Z', -10))
    
    def One_movement(self):
        self.XPos_pushButton.clicked.connect(lambda: self.move_axis('X', 1))
        self.XNeg_pushButton.clicked.connect(lambda: self.move_axis('X', -1))
        self.YPos_pushButton.clicked.connect(lambda: self.move_axis('Y', 1))
        self.YNeg_pushButton.clicked.connect(lambda: self.move_axis('Y', -1))
        self.ZPos_pushButton.clicked.connect(lambda: self.move_axis('Z', 1))
        self.ZNeg_pushButton.clicked.connect(lambda: self.move_axis('Z', -1))
    
    def DotOne_movement(self):
        self.XPos_pushButton.clicked.connect(lambda: self.move_axis('X', 0.1))
        self.XNeg_pushButton.clicked.connect(lambda: self.move_axis('X', -0.1))
        self.YPos_pushButton.clicked.connect(lambda: self.move_axis('Y', 0.1))
        self.YNeg_pushButton.clicked.connect(lambda: self.move_axis('Y', -0.1))
        self.ZPos_pushButton.clicked.connect(lambda: self.move_axis('Z', 0.1))
        self.ZNeg_pushButton.clicked.connect(lambda: self.move_axis('Z', -0.1))

    def move_axis(self, axis, distance):
        gcode_command = f"G0{axis}{distance:+06.1f}"
        current_time = datetime.now().strftime('%H:%M:%S')
        self.Status_textBrowser.append(f"[{current_time}] {axis} go {distance} mm") 
        self.send_to_arduino(gcode_command)

        if axis == 'X':
            self.M_CurrentPos[0] = M_CurrentPos[0] + distance
        elif axis == 'Y':
            self.M_CurrentPos[1] = M_CurrentPos[1] + distance
        elif axis == 'Z':
            self.M_CurrentPos[2] = M_CurrentPos[2] + distance


    def disable_move_buttons(self):
        self.XPos_pushButton.setEnabled(False)
        self.XNeg_pushButton.setEnabled(False)
        self.YPos_pushButton.setEnabled(False)
        self.YNeg_pushButton.setEnabled(False)
        self.ZPos_pushButton.setEnabled(False)
        self.ZNeg_pushButton.setEnabled(False)
                

    def enable_move_buttons(self):
        self.XPos_pushButton.setEnabled(True)
        self.XNeg_pushButton.setEnabled(True)
        self.YPos_pushButton.setEnabled(True)
        self.YNeg_pushButton.setEnabled(True)
        self.ZPos_pushButton.setEnabled(True)
        self.ZNeg_pushButton.setEnabled(True)
        

    def update_speed_label(self):
        slider_value = self.Speed_horizontalSlider.value()  # Get the current slider value
        speeds = {
            1: (100, 100, 50),
            2: (125, 125, 50),
            3: (150, 150, 50),
            4: (175, 175, 50),
            5: (200, 200, 50)
        }
        x_speed, y_speed, z_speed = speeds.get(slider_value, (100, 100, 50))  # Default 
        current_time = datetime.now().strftime('%H:%M:%S')
        self.label_22.setText(f"{x_speed}, {y_speed}, {z_speed}")
        self.Status_textBrowser.append(f"[{current_time}] Speed set at {x_speed}, {y_speed}, {z_speed} (mm/min)")


    def update_speed_label1(self):
        slider_value = self.Speed_horizontalSlider.value()  # Get the current slider value
        speed_commands = {
            1: "S1",
            2: "S2",
            3: "S3",
            4: "S4",
            5: "S5"
        }
        speed_command = speed_commands.get(slider_value, "S1")  # Default to SS1 if value not found
        self.send_speed_to_arduino(speed_command)


    def send_speed_to_arduino(self, speed_command):
        if hasattr(self, 'ser') and self.ser.is_open:
            try:
                self.ser.write(f"{speed_command}\n".encode())  # Convert to bytes and send
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Sent speed command: {speed_command}")
            except Exception as e:
                self.Status_textBrowser.append(f"Error sending speed command: {e}")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def update_accel_label(self):
        slider_value = self.Acceleration_horizontalSlider.value()  # Get the current slider value
        accel = {
            1: (200, 200),
            2: (250, 250),
            3: (300, 300),
            4: (350, 350),
            5: (400, 400)
        }
        x_accel, y_accel = accel.get(slider_value, (200, 200))  # Default 

        self.label_23.setText(f"{x_accel}, {y_accel}")
        self.Status_textBrowser.append(f"Acceleration set at {x_accel}, {y_accel}  (mm/min^2)")

    def update_accel_label1(self):
        slider_value = self.Acceleration_horizontalSlider.value()  # Get the current slider value
        accel_commands = {
            1: "A1",
            2: "A2",
            3: "A3",
            4: "A4",
            5: "A5"
        }
        accel_command = accel_commands.get(slider_value, "A1")  # Default to SA1 if value not found
        self.send_accel_to_arduino(accel_command)


    def send_accel_to_arduino(self, accel_command):
        if hasattr(self, 'ser') and self.ser.is_open:
            try:
                self.ser.write(f"{accel_command}\n".encode())  # Convert to bytes and send
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Sent acceleration command: {accel_command}")
            except Exception as e:
                self.Status_textBrowser.append(f"Error sending acceleration command: {e}")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def check_available(self):
        if self.Connect_pushButton.text() == "Disconnect" and self.IsMoving == 1:
            data = self.read_from_serial_port()
            if data is not None and data.strip() == 'Done':  # Check if 'Done' message is received
                self.Enable_Function()
                self.IsMoving = 0

    def Disable_Function(self):
        self.tab.setEnabled(False)

    def Enable_Function(self): 
        if self.AdjustFlag == 1:
            self.Status_textBrowser.append(datetime.now().strftime("[%H:%M:%S]: ") +"Successful")  
            self.AdjustFlag = 0
        else:
            self.Status_textBrowser.append(datetime.now().strftime("[%H:%M:%S]: ") +"DONE")  
            self.tab.setEnabled(True)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

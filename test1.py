from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
import serial
import serial.tools.list_ports
from datetime import datetime
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

DegValidator = QtGui.QDoubleValidator(
                -9999.0, # bottom
                9999.0, # top
                3, # decimals 
                notation=QtGui.QDoubleValidator.StandardNotation)

OnlyFloat = QtGui.QDoubleValidator(
                -9999.0, # bottom
                9999.0, # top
                3, # decimals 
                notation=QtGui.QDoubleValidator.StandardNotation)

DegValidator.setRange(-9999.0, 9999.0)  # Set the range for integer input


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # config interface
        self.IsMoving = 0
        self.IsMoving_1 = 0
        self.displacement = [0,0]
        self.Zoffset = 0
        self.Is_Move_Frame = 0
        self.current_command_index = 0
        self.Z_Current_State = 0
        self.widget = QWidget
        self.x_coords = []
        self.y_coords = []
        self.Zoffset = 0
        self.current_command_index = 0
        self.previous_x = 0
        self.previous_y = 0
        self.gcode_commands = []
        self.Z_Current_State = 0
        self.M_CurrentPos = [0, 0, 0]
        self.Machine_Max_UpperLim = [205,190]
        self.Machine_Max_LowerLim= [-205,-190]
        self.Current_X_Gcode = 0
        self.Current_Y_Gcode = 0

        
        #--------------# config widget 
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 781)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1021, 741))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.COM_comboBox = QtWidgets.QComboBox(self.tab)
        self.COM_comboBox.setGeometry(QtCore.QRect(140, 40, 83, 22))
        self.COM_comboBox.setObjectName("COM_comboBox")
        self.Baudrate_comboBox = QtWidgets.QComboBox(self.tab)
        self.Baudrate_comboBox.setGeometry(QtCore.QRect(140, 70, 83, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Baudrate_comboBox.setFont(font)
        self.Baudrate_comboBox.setObjectName("Baudrate_comboBox")
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
        self.YPos_pushButton.setGeometry(QtCore.QRect(500, 240, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.YPos_pushButton.setFont(font)
        self.YPos_pushButton.setObjectName("YPos_pushButton")
        self.YNeg_pushButton = QtWidgets.QPushButton(self.tab)
        self.YNeg_pushButton.setGeometry(QtCore.QRect(500, 350, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.YNeg_pushButton.setFont(font)
        self.YNeg_pushButton.setObjectName("YNeg_pushButton")
        self.XNeg_pushButton = QtWidgets.QPushButton(self.tab)
        self.XNeg_pushButton.setGeometry(QtCore.QRect(390, 300, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.XNeg_pushButton.setFont(font)
        self.XNeg_pushButton.setObjectName("XNeg_pushButton")
        self.XPos_pushButton = QtWidgets.QPushButton(self.tab)
        self.XPos_pushButton.setGeometry(QtCore.QRect(610, 300, 70, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.XPos_pushButton.setFont(font)
        self.XPos_pushButton.setObjectName("XPos_pushButton")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(270, 280, 101, 141))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
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
        self.label_6.setGeometry(QtCore.QRect(260, 60, 30, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(260, 120, 30, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(260, 140, 30, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.X_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.X_lineEdit.setGeometry(QtCore.QRect(300, 70, 113, 22))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.X_lineEdit.setFont(font)
        self.X_lineEdit.setObjectName("X_lineEdit")
        self.X_lineEdit.setValidator(OnlyFloat)
        self.X_lineEdit.setText(f"{self.M_CurrentPos[0]:.3f}")
        self.Y_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.Y_lineEdit.setGeometry(QtCore.QRect(300, 130, 113, 22))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.Y_lineEdit.setFont(font)
        self.Y_lineEdit.setObjectName("Y_lineEdit")
        self.Y_lineEdit.setValidator(OnlyFloat)
        self.Y_lineEdit.setText(f"{self.M_CurrentPos[1]:.3f}")
        self.XHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.XHome_pushButton.setGeometry(QtCore.QRect(430, 65, 70, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.XHome_pushButton.setFont(font)
        self.XHome_pushButton.setObjectName("XHome_pushButton")
        self.YHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.YHome_pushButton.setGeometry(QtCore.QRect(430, 125, 70, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.YHome_pushButton.setFont(font)
        self.YHome_pushButton.setObjectName("YHome_pushButton")
        self.AllHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.AllHome_pushButton.setGeometry(QtCore.QRect(390, 190, 100, 30))
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
        self.Gcode_textBrowser.setGeometry(QtCore.QRect(520, 60, 291, 41))
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
        self.X_Calibrate_pushButton = QtWidgets.QPushButton(self.tab)
        self.X_Calibrate_pushButton.setGeometry(QtCore.QRect(70, 200, 93, 28))
        self.X_Calibrate_pushButton.setObjectName("X_Calibrate_pushButton")
        self.Y_Calibrate_pushButton = QtWidgets.QPushButton(self.tab)
        self.Y_Calibrate_pushButton.setGeometry(QtCore.QRect(70, 250, 93, 28))
        self.Y_Calibrate_pushButton.setObjectName("Y_Calibrate_pushButton")
        self.Move_pushButton = QtWidgets.QPushButton(self.tab)
        self.Move_pushButton.setGeometry(QtCore.QRect(280, 190, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Move_pushButton.setFont(font)
        self.Move_pushButton.setObjectName("Move_pushButton")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_2.setGeometry(QtCore.QRect(5, 440, 1006, 261))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.All_Calibrate_pushButton = QtWidgets.QPushButton(self.tab)
        self.All_Calibrate_pushButton.setGeometry(QtCore.QRect(70, 300, 93, 28))
        self.All_Calibrate_pushButton.setObjectName("All_Calibrate_pushButton")
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
        self.Status_textBrowser.setGeometry(QtCore.QRect(14, 480, 991, 211))
        self.Status_textBrowser.setObjectName("Status_textBrowser")
        self.ClearMessage_pushButton = QtWidgets.QPushButton(self.tab)
        self.ClearMessage_pushButton.setGeometry(QtCore.QRect(885, 450, 121, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.ClearMessage_pushButton.setFont(font)
        self.ClearMessage_pushButton.setObjectName("ClearMessage_pushButton")
        self.Command_textBrowser = QtWidgets.QTextBrowser(self.tab_2)
        self.Command_textBrowser.setGeometry(QtCore.QRect(690, 330, 301, 341))
        self.Command_textBrowser.setObjectName("Command_textBrowser")
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
        self.photo.setGeometry(QtCore.QRect(930, 20, 61, 61))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("logo.png"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(810, 250, 51, 16))
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
        self.label_18 = QtWidgets.QLabel(self.tab)
        self.label_18.setGeometry(QtCore.QRect(720, 280, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.ZOffset_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.ZOffset_lineEdit.setGeometry(QtCore.QRect(788, 277, 61, 22))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.ZOffset_lineEdit.setFont(font)
        self.ZOffset_lineEdit.setObjectName("ZOffset_lineEdit")
        self.Save_pushButton = QtWidgets.QPushButton(self.tab)
        self.Save_pushButton.setGeometry(QtCore.QRect(900, 275, 73, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Save_pushButton.setFont(font)
        self.Save_pushButton.setObjectName("Save_pushButton")
        self.ZPos_pushButton = QtWidgets.QPushButton(self.tab)
        self.ZPos_pushButton.setGeometry(QtCore.QRect(808, 330, 42, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(75)
        self.ZPos_pushButton.setFont(font)
        self.ZPos_pushButton.setObjectName("ZPos_pushButton")
        self.ZNeg_pushButton = QtWidgets.QPushButton(self.tab)
        self.ZNeg_pushButton.setGeometry(QtCore.QRect(758, 330, 42, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(75)
        self.ZNeg_pushButton.setFont(font)
        self.ZNeg_pushButton.setObjectName("ZNeg_pushButton")
        self.Z_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.Z_lineEdit.setGeometry(QtCore.QRect(788, 305, 61, 22))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.Z_lineEdit.setFont(font)
        self.Z_lineEdit.setObjectName("Z_lineEdit")
        self.Z_lineEdit.setValidator(OnlyFloat)
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
        self.Acceleration_horizontalSlider = QtWidgets.QSlider(self.tab)
        self.Acceleration_horizontalSlider.setGeometry(QtCore.QRect(20, 400, 140, 22))
        self.Acceleration_horizontalSlider.setMinimum(1)
        self.Acceleration_horizontalSlider.setMaximum(5)
        self.Acceleration_horizontalSlider.setPageStep(1)
        self.Acceleration_horizontalSlider.setProperty("value", 1)
        self.Acceleration_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.Acceleration_horizontalSlider.setObjectName("Acceleration_horizontalSlider")
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
        self.label_24 = QtWidgets.QLabel(self.tab)
        self.label_24.setGeometry(QtCore.QRect(720, 308, 51, 16))
        self.label_24.setObjectName("label_24")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.label_24.setFont(font)
        self.Start_pushButton = QtWidgets.QPushButton(self.tab)
        self.Start_pushButton.setGeometry(QtCore.QRect(720, 110, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Start_pushButton.setFont(font)
        self.Start_pushButton.setObjectName("Start_pushButton")
        self.label_25 = QtWidgets.QLabel(self.tab)
        self.label_25.setGeometry(QtCore.QRect(860, 280, 51, 16))
        self.label_25.setObjectName("label_25")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.label_25.setFont(font)
        self.label_26 = QtWidgets.QLabel(self.tab)
        self.label_26.setGeometry(QtCore.QRect(860, 305, 51, 16))
        self.label_26.setObjectName("label_25")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.label_26.setFont(font)
        self.SetHome_pushButton = QtWidgets.QPushButton(self.tab)
        self.SetHome_pushButton.setGeometry(QtCore.QRect(720, 110, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.SetHome_pushButton.setFont(font)
        self.SetHome_pushButton.setObjectName("SetHome_pushButton")
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
        self.groupBox.raise_()
        self.line.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.X_lineEdit.raise_()
        self.Y_lineEdit.raise_()
        self.XHome_pushButton.raise_()
        self.YHome_pushButton.raise_()
        self.AllHome_pushButton.raise_()
        self.line_2.raise_()
        self.label_10.raise_()
        self.Gcode_textBrowser.raise_()
        self.Load_pushButton.raise_()
        self.Delete_pushButton.raise_()
        self.tableView_4.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.ManualCommand_lineEdit.raise_()
        self.Send_pushButton.raise_()
        self.X_Calibrate_pushButton.raise_()
        self.Y_Calibrate_pushButton.raise_()
        self.Move_pushButton.raise_()
        self.textBrowser_2.raise_()
        self.All_Calibrate_pushButton.raise_()
        self.label_9.raise_()
        self.Status_textBrowser.raise_()
        self.ClearMessage_pushButton.raise_()
        self.Command_textBrowser.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.photo.raise_()
        self.label_15.raise_()
        self.line_3.raise_()
        self.label_18.raise_()
        self.ZOffset_lineEdit.raise_()
        self.Save_pushButton.raise_()
        self.ZPos_pushButton.raise_()
        self.ZNeg_pushButton.raise_()
        self.Z_lineEdit.raise_()
        self.label_20.raise_()
        self.label_21.raise_()
        self.Speed_horizontalSlider.raise_()
        self.Acceleration_horizontalSlider.raise_()
        self.label_22.raise_()
        self.label_23.raise_()
        self.label_24.raise_()
        self.label_25.raise_()
        self.label_26.raise_()
        self.SetHome_pushButton.raise_()
        self.tabWidget.addTab(self.tab, "")     
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableView_3 = QtWidgets.QTableView(self.tab_2)
        self.tableView_3.setGeometry(QtCore.QRect(5, 10, 1001, 691))
        self.tableView_3.setObjectName("tableView_3")
        self.widget = QtWidgets.QWidget(self.tab_2)
        self.widget.setGeometry(QtCore.QRect(10, 20, 661, 661))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.widget.setFont(font)
        self.widget.setObjectName("widget")
        self.Start_pushButton = QtWidgets.QPushButton(self.tab_2)
        self.Start_pushButton.setGeometry(QtCore.QRect(680, 20, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Start_pushButton.setFont(font)
        self.Start_pushButton.setObjectName("Start_pushButton")
        self.Frame_pushButton = QtWidgets.QPushButton(self.tab_2)
        self.Frame_pushButton.setGeometry(QtCore.QRect(780, 20, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.Frame_pushButton.setFont(font)
        self.Frame_pushButton.setObjectName("Frame_pushButton")
        self.listView = QtWidgets.QListView(self.tab_2)
        self.listView.setGeometry(QtCore.QRect(680, 350, 321, 331))
        self.listView.setObjectName("listView")
        self.Command_textBrowser = QtWidgets.QTextBrowser(self.tab_2)
        self.Command_textBrowser.setGeometry(QtCore.QRect(690, 390, 301, 281))
        self.Command_textBrowser.setObjectName("Command_textBrowser")
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(690, 360, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.ClearMessage_pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.ClearMessage_pushButton_2.setGeometry(QtCore.QRect(870, 70, 121, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.ClearMessage_pushButton_2.setFont(font)
        self.ClearMessage_pushButton_2.setObjectName("ClearMessage_pushButton_2")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(690, 60, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.listView_2 = QtWidgets.QListView(self.tab_2)
        self.listView_2.setGeometry(QtCore.QRect(680, 50, 321, 291))
        self.listView_2.setObjectName("listView_2")
        self.Status_textBrowser_2 = QtWidgets.QTextBrowser(self.tab_2)
        self.Status_textBrowser_2.setGeometry(QtCore.QRect(690, 100, 301, 231))
        self.Status_textBrowser_2.setObjectName("Status_textBrowser_2")
        self.tableView_3.raise_()
        self.widget.raise_()
        self.Start_pushButton.raise_()
        self.listView.raise_()
        self.Command_textBrowser.raise_()
        self.listView_2.raise_()
        self.Status_textBrowser_2.raise_()
        self.ClearMessage_pushButton_2.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.Frame_pushButton.raise_()
        self.tabWidget.addTab(self.tab_2, "")
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


        self.Refresh_pushButton.clicked.connect(self.refresh_ports)
        self.Connect_pushButton.clicked.connect(self.connect_or_disconnect)
        self.Load_pushButton.clicked.connect(self.load_and_process_file)
        self.Delete_pushButton.clicked.connect(self.unload_file)
        self.Move_pushButton.clicked.connect(self.move_command)
        self.ClearMessage_pushButton.clicked.connect(self.clear_messages)
        self.XPos_pushButton.clicked.connect(self.move_X_positive)
        self.XNeg_pushButton.clicked.connect(self.move_X_negative)
        self.YPos_pushButton.clicked.connect(self.move_Y_positive)
        self.YNeg_pushButton.clicked.connect(self.move_Y_negative) 
        self.ZNeg_pushButton.clicked.connect(self.move_Z_negative)    
        self.ZPos_pushButton.clicked.connect(self.move_Z_positive) 
        self.Save_pushButton.clicked.connect(self.save_Z_offset)
        self.Hundred_radioButton.clicked.connect(lambda: self.display_distance_message(100))
        self.Ten_radioButton.clicked.connect(lambda: self.display_distance_message(10))
        self.One_radioButton.clicked.connect(lambda: self.display_distance_message(1))
        self.DotOne_radioButton.clicked.connect(lambda: self.display_distance_message(0.1))
        self.Speed_horizontalSlider.sliderReleased.connect(self.update_speed_label)
        self.Speed_horizontalSlider.sliderReleased.connect(self.update_speed_label1)
        self.Acceleration_horizontalSlider.sliderReleased.connect(self.update_accel_label)
        self.Acceleration_horizontalSlider.sliderReleased.connect(self.update_accel_label1)
        self.Send_pushButton.clicked.connect(self.send_command)
        self.Start_pushButton.clicked.connect(self.start_processing)
        self.X_Calibrate_pushButton.clicked.connect(self.calibrate_X)
        self.Y_Calibrate_pushButton.clicked.connect(self.calibrate_Y)
        self.All_Calibrate_pushButton.clicked.connect(self.calibrate_All)
        self.SetHome_pushButton.clicked.connect(self.Set_Home)
        self.Frame_pushButton.clicked.connect(self.frame)
    #---------------------CHECK MESSAGE---------#
        #timer
        self.timer1 = QTimer(self.tab)
        self.timer1.timeout.connect(self.check_available)
        self.timer1.start(0)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CNC Controller"))
        self.Baudrate_comboBox.setItemText(0, _translate("MainWindow", "115200"))
        self.label.setText(_translate("MainWindow", "Serial Configuration"))
        self.label_2.setText(_translate("MainWindow", "COM:"))
        self.label_3.setText(_translate("MainWindow", "Baudrate:"))
        self.Refresh_pushButton.setText(_translate("MainWindow", "Refresh"))
        self.Connect_pushButton.setText(_translate("MainWindow", "Connect"))
        self.label_4.setText(_translate("MainWindow", "Jogging"))
        self.YPos_pushButton.setText(_translate("MainWindow", "Y +"))
        self.YNeg_pushButton.setText(_translate("MainWindow", "Y -"))
        self.XNeg_pushButton.setText(_translate("MainWindow", "X -"))
        self.XPos_pushButton.setText(_translate("MainWindow", "X +"))
        self.groupBox.setTitle(_translate("MainWindow", "Distance"))
        self.Hundred_radioButton.setText(_translate("MainWindow", "100"))
        self.Ten_radioButton.setText(_translate("MainWindow", "10"))
        self.One_radioButton.setText(_translate("MainWindow", "1"))
        self.DotOne_radioButton.setText(_translate("MainWindow", "0.1"))
        self.label_5.setText(_translate("MainWindow", "Work"))
        self.label_6.setText(_translate("MainWindow", "X"))
        self.label_7.setText(_translate("MainWindow", "Y"))
        self.X_lineEdit.setText(_translate("MainWindow", "0.000"))
        self.Y_lineEdit.setText(_translate("MainWindow", "0.000"))
        self.XHome_pushButton.setText(_translate("MainWindow", "Set 0"))
        self.XHome_pushButton.clicked.connect(self.X_Home)
        self.YHome_pushButton.setText(_translate("MainWindow", "Set 0"))
        self.YHome_pushButton.clicked.connect(self.Y_Home)
        self.AllHome_pushButton.setText(_translate("MainWindow", "Home All"))
        self.AllHome_pushButton.clicked.connect(self.Home_All)
        self.label_10.setText(_translate("MainWindow", "G-Code"))
        self.Load_pushButton.setText(_translate("MainWindow", "Load"))
        self.Delete_pushButton.setText(_translate("MainWindow", "Delete"))
        self.label_11.setText(_translate("MainWindow", "Basic control"))
        self.label_12.setText(_translate("MainWindow", "Manual Command"))
        self.Send_pushButton.setText(_translate("MainWindow", "Send"))
        self.X_Calibrate_pushButton.setText(_translate("MainWindow", "X Calibrate"))
        self.Y_Calibrate_pushButton.setText(_translate("MainWindow", "Y Calibrate"))
        self.Move_pushButton.setText(_translate("MainWindow", "Move"))
        self.All_Calibrate_pushButton.setText(_translate("MainWindow", "Calibrate All"))
        self.label_9.setText(_translate("MainWindow", "Status"))
        self.ClearMessage_pushButton.setText(_translate("MainWindow", "Clear Message"))
        self.label_13.setText(_translate("MainWindow", "By Nguyen Hoang Khang "))
        self.label_14.setText(_translate("MainWindow", "EEACIU19015 - HCMIU"))
        self.label_15.setText(_translate("MainWindow", "Offset"))
        self.label_16.setText(_translate("MainWindow", "List Command"))
        self.label_18.setText(_translate("MainWindow", "Z Offset:"))
        self.Save_pushButton.setText(_translate("MainWindow", "Save"))
        self.ZPos_pushButton.setText(_translate("MainWindow", "Z +"))
        self.ZNeg_pushButton.setText(_translate("MainWindow", "Z -"))
        self.ZOffset_lineEdit.setText(_translate("MainWindow", "0.0"))
        self.Z_lineEdit.setText(_translate("MainWindow", "0.0"))
        self.label_20.setText(_translate("MainWindow", "Speed:"))
        self.label_21.setText(_translate("MainWindow", "Acceleration:"))
        self.label_22.setText(_translate("MainWindow", "100, 100, 50"))
        self.label_23.setText(_translate("MainWindow", "200, 200"))
        self.label_24.setText(_translate("MainWindow", "IncVal:"))
        self.label_25.setText(_translate("MainWindow", "mm"))
        self.label_26.setText(_translate("MainWindow", "mm"))
        self.SetHome_pushButton.setText(_translate("MainWindow", "Set Home"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Interface"))
        self.Start_pushButton.setText(_translate("MainWindow", "Start"))
        self.Frame_pushButton.setText(_translate("MainWindow", "Frame"))
        self.label_16.setText(_translate("MainWindow", "List command"))
        self.ClearMessage_pushButton_2.setText(_translate("MainWindow", "Clear Message"))
        self.label_17.setText(_translate("MainWindow", "Status 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "G Code "))
        self.menuFILE.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))

    def exit_application(self):
        self.MainWindow.close()
        
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
    
    def refresh_ports(self):
        # Clear and repopulate COM ports
        self.COM_comboBox.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.COM_comboBox.addItem(port.device)
    
    def clear_messages(self):
        # Clear the content of the SystemM_textBrowser
        self.Status_textBrowser.clear()

    def read_from_serial_port(self):
        try:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode().strip()
                if data == 'Ok' or data == 'EB':
                    return data
        except serial.SerialException as e:
            print(f"Failed to read from serial port: {e}")
            return None
        
    def check_available(self):
        if self.Connect_pushButton.text() == "Disconnect":
            data = self.read_from_serial_port()
            if data is not None and data.strip() == 'Ok' and self.IsMoving == 1:  # Check if 'Ok' message is received     
                if self.current_command_index < len(self.gcode_commands):
                    self.process_next_command()
                else: 
                    self.Enable_Function()
                    self.IsMoving = 0
            elif data is not None and data.strip() == 'Ok' and self.IsMoving_1 == 1:  # Check if 'Ok' message is received
                    self.Enable_Function()
                    self.IsMoving_1 = 1
            elif data is not None and data.strip() == 'Ok' and self.Is_Move_Frame == 1:  # Check if 'Ok' message is received
                if self.edge_index < len(self.rect_coords):
                    print("Send " + str(self.edge_index)+ "line")
                    self.draw_next_edge()

                else:
                    self.Is_Move_Frame = 0
                    self.Enable_Function()
                    self.remove_frame()
                    

            if data is not None and data.strip() == 'EB':
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] ALLERT !!! EMERGENCY BUTTON PRESSED !!!")


    def start_processing(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving = 1
            if len(self.gcode_commands) == 0:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] No G-code commands loaded")
                return
            self.current_command_index  = 0
            self.process_next_command()
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def extract_coordinates(self, command):
        # Define start and end position of X and Y in list G-code
        x_start = command.find('X') + 1
        x_end = command.find('Y')
        y_start = command.find('Y') + 1
        y_end = command.find('Z') if 'Z' in command else len(command)

        # Take out the value of X and Y from list G-code
        x = float(command[x_start:x_end]) if x_start < x_end else 0.0
        y = float(command[y_start:y_end]) if y_start < y_end else 0.0

        return x, y
    
    def update_current_position(self):
        # Take the last G-code line
        if self.current_command_index > 0:
            last_command = self.gcode_commands[self.current_command_index - 1]
            x_mm, y_mm = self.extract_coordinates(last_command)
            self.M_CurrentPos[0] = x_mm
            self.M_CurrentPos[1] = y_mm

    def plot_coordinates(self, command):
        # Extract X and Y coordinates from the command
        x_start = command.find('X') + 1
        x_end = command.find('Y')
        y_start = command.find('Y') + 1
        y_end = command.find('Z') if 'Z' in command else len(command)

        if x_start != -1 and x_end != -1 and y_start != -1 and (y_end != -1 or 'Z' not in command):
            try:
                x = float(command[x_start:x_end])
                y = float(command[y_start:y_end])

                # Clear the previous marker
                if hasattr(self, 'marker') and self.marker:
                    self.marker.remove()

                # Add the red '+' marker at the new position
                self.marker, = self.ax.plot(x, y, marker='+', color='red', markersize=20)
                self.fig.canvas.draw()

            except ValueError:
                pass

                    
    def process_next_command(self):
        if self.current_command_index < len(self.gcode_commands) and self.IsMoving == 1:
            command = self.gcode_commands[self.current_command_index]
            steps = self.convert_command_to_steps_1(command)
            if command[1] == '0':
                if self.Z_Current_State == 0:
                    ZtoMove = 0
                else:
                    ZtoMove = -self.Zoffset
                    self.Z_Current_State = 0

                gcode_send = "G0X{:0=+}Y{:0=+}Z{:0=+}".format(steps[0], steps[1], (ZtoMove))
                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_send)
                # Simulate movement by updating plot position
                x = steps[0]
                y = steps[1]

            elif command[1] == '1':
                if self.Z_Current_State == 0:
                    ZtoMove = self.Zoffset
                    self.Z_Current_State = 1
                else:
                    ZtoMove = 0

                gcode_send = "G0X{:0=+}Y{:0=+}Z{:0=+}".format(steps[0], steps[1], (ZtoMove))
                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_send)
                # Simulate movement by updating plot position
                x = steps[0]
                y = steps[1]
            self.plot_coordinates(command)
            self.current_command_index += 1
            if self.current_command_index == len(self.gcode_commands):
                self.update_current_position()
                
    def Set_Home(self):
        print([self.M_CurrentPos[0],self.M_CurrentPos[1]])
        self.displacement[0] = self.M_CurrentPos[0]
        self.displacement[1] = self.M_CurrentPos[1]

    def convert_command_to_steps_1(self, command):
        x_coord_v = self.get_coord_value(command, 'X', self.M_CurrentPos[0])
        y_coord_v = self.get_coord_value(command, 'Y', self.M_CurrentPos[1])
        # Limit coordinate value
        x_coord_v = min(max(x_coord_v, self.Machine_Max_LowerLim[0]), self.Machine_Max_UpperLim[0])
        y_coord_v = min(max(y_coord_v, self.Machine_Max_LowerLim[1]), self.Machine_Max_UpperLim[1])


        # Calculate steps to move
        x_ToMove = x_coord_v + self.displacement[0]  - self.M_CurrentPos[0]
        y_ToMove = y_coord_v + self.displacement[1]  - self.M_CurrentPos[1]


        # Cập nhật vị trí gốc mới    
        self.M_CurrentPos[0] = x_coord_v + self.displacement[0]
        self.M_CurrentPos[1] = y_coord_v + self.displacement[1]
        # Set lineEdits for current position
        self.X_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[0]))
        self.Y_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[1]))

        steps = self.calculate_steps_to_move(x_ToMove, y_ToMove, 0.0)
        return steps

    
    def load_and_process_file(self):
        if self.Connect_pushButton.text() == "Disconnect":
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(None, "Load G-code file", "", 
                                                    "G-Code Files (*.ngc);;Text Files (*.txt);;All Files (*)", options=options)
            if fileName:
                with open(fileName, 'r') as file:
                    lines = file.readlines()
                    gcode_commands = []
                    current_x, current_y = 0.0, 0.0

                    for line in lines:
                        line = line.strip()
                        if line.startswith('G'):
                            if 'Z' in line:
                                continue  # Skip lines containing Z coordinates
                            if line.startswith('G1') or line.startswith('G0'):
                                x_end = self.get_coord_value(line, 'X', current_x)
                                y_end = self.get_coord_value(line, 'Y', current_y)
                                if line.startswith('G1'):
                                    segments = self.interpolate(current_x, current_y, x_end, y_end)
                                    for x, y in segments:
                                        gcode_commands.append(f"G1 X {x:.3f} Y {y:.3f}")
                                else:  # G0 command
                                    line = ' '.join(line.split())  # Clean up multiple spaces
                                    gcode_commands.append(line)
                                current_x, current_y = x_end, y_end

                    # Clear and populate the Command_textBrowser with G-code commands
                    self.Command_textBrowser.clear()
                    for command in gcode_commands:
                        self.Command_textBrowser.append(command)

                    # Update status and display loaded file name in the GUI
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Loaded G-code file")
                    self.Status_textBrowser_2.append(f"[{current_time}] Loaded G-code file")
                    self.Gcode_textBrowser.append(f"{fileName}")

                    # Store the loaded G-code commands in self.gcode_commands for further processing
                    self.gcode_commands = gcode_commands
                    print(self.gcode_commands)  # Optional: Print the loaded G-code commands
                    self.plot_gcode_commands(self.gcode_commands)

            else:
                # Inform user if no file was selected
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] No file selected")
        else:
            # Inform user if Arduino is not connected
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def unload_file(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.Gcode_textBrowser.clear()
            self.Command_textBrowser.clear()
            self.gcode_commands.clear()
            self.clear_plot_on_tab2()
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Unloaded the file")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def interpolate(self, x_start, y_start, x_end, y_end, max_segment_length=0.2):
        distance = ((x_end - x_start) ** 2 + (y_end - y_start) ** 2) ** 0.5
        num_segments = max(1, int(self.custom_round(distance / max_segment_length)))
        
        x_segments = [(x_start + i * (x_end - x_start) / num_segments) for i in range(1, num_segments + 1)]
        y_segments = [(y_start + i * (y_end - y_start) / num_segments) for i in range(1, num_segments + 1)]
        
        # Adjust the last segment if it's smaller than max_segment_length
        if num_segments > 1:
            last_segment_length = ((x_segments[-1] - x_segments[-2]) ** 2 + (y_segments[-1] - y_segments[-2]) ** 2) ** 0.5
            if last_segment_length < max_segment_length:
                x_segments[-2] = x_end
                y_segments[-2] = y_end
                x_segments.pop(-1)
                y_segments.pop(-1)
        
        return list(zip(x_segments, y_segments))

    def move_Z_positive(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1= 1
            try:
                z_move_value = float(self.Z_lineEdit.text())
                self.move_Z(z_move_value)
            except ValueError:
                self.Status_textBrowser.append("Invalid input for Z movement")
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def move_Z_negative(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            try:
                z_move_value = float(self.Z_lineEdit.text())
                self.move_Z(-z_move_value)
            except ValueError:
                self.Status_textBrowser.append("Invalid input for Z movement")
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def move_Z(self, z_move_value):
        if self.Connect_pushButton.text() == "Disconnect":
            steps = self.calculate_steps_to_move(0, 0, z_move_value)
            gcode_send = "G0Z{:0=+}".format(int(steps[2]))
            self.send_to_arduino(gcode_send)
            self.display_gcode(gcode_send)
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def save_Z_offset(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.Z_Current_State = 1
            if self.ZOffset_lineEdit.text():
                self.Zoffset = float(self.ZOffset_lineEdit.text())* (400 / 8)
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Save value for Z offset = "+ self.ZOffset_lineEdit.text()+ "mm")
            else:
                return
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def move_command(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            command = "G0"
            # X coordinate
            if self.X_lineEdit.text():
                x_value = float(self.X_lineEdit.text())
                command += f" X{x_value:.3f}" 

            # Y coordinate
            if self.Y_lineEdit.text():
                y_value = float(self.Y_lineEdit.text())
                command += f" Y{y_value:.3f}"

            # Convert command to steps and round them
            steps = self.convert_command_to_steps(command)

            if len(steps) >= 2: 
                x_ToMove, y_ToMove = steps[:2]
                gcode_send = "G0X{:0=+}Y{:0=+}".format(int(x_ToMove), int(y_ToMove))
                gcode_display = "G0X{:0=+}Y{:0=+}".format(x_ToMove, y_ToMove)

                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_display)
            else:
                self.Status_textBrowser.append("Error: Insufficient steps provided")

            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")


    def send_command(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            command = self.ManualCommand_lineEdit.text().strip().upper()
            command = command.replace(" ", "")
            
            if not command.startswith("G0"):
                self.Status_textBrowser.append("Error: Invalid G-code format")
                return

            steps = self.convert_command_to_steps(command)

            if len(steps) >= 2: 
                x_ToMove, y_ToMove = steps[:2]
                gcode_send = "G0X{:0=+}Y{:0=+}".format(int(steps[0]), int(steps[1]))
                gcode_display = "G0X{:0=+}Y{:0=+}".format(x_ToMove, y_ToMove)
                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_display)
            else:
                self.Status_textBrowser.append("Error: Insufficient steps provided")
            
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")
    
    def convert_command_to_steps(self, command):
        x_coord_v = self.get_coord_value(command, 'X', self.M_CurrentPos[0] )
        y_coord_v = self.get_coord_value(command, 'Y', self.M_CurrentPos[1])

        # Limit coordinate value
        x_coord_v = min(max(x_coord_v, self.Machine_Max_LowerLim[0]), self.Machine_Max_UpperLim[0])
        y_coord_v = min(max(y_coord_v, self.Machine_Max_LowerLim[1]), self.Machine_Max_UpperLim[1])

        # Calculate steps to move
        x_ToMove = x_coord_v - self.M_CurrentPos[0]
        y_ToMove = y_coord_v - self.M_CurrentPos[1]

        self.M_CurrentPos[0] = x_coord_v
        self.M_CurrentPos[1] = y_coord_v

        # Set lineEdits for current position
        self.X_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[0]))
        self.Y_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[1]))

        steps = self.calculate_steps_to_move(x_ToMove, y_ToMove, 0.0)
        return steps

    def get_coord_value(self, command, axis, current_value):
        if axis in command:
            index = command.index(axis) + 1
            coord_str = ''
            while index < len(command) and (command[index].isdigit() or command[index] == '.' or command[index] == '-' or command[index] ==  ' '):
                coord_str += command[index]
                index += 1
            if coord_str:
                return float(coord_str)
        return current_value
    
    def custom_round(self, float_number):
        integer_part = int(float_number)
        decimal_part = abs(float_number - integer_part)
        if decimal_part >= 0.5:
            return integer_part + (1 if float_number >= 0 else -1)
        else:
            return integer_part

    def calculate_steps_to_move(self, x_ToMove, y_ToMove, z_ToMove):
        # Calculate the steps to move for each axis
        Stp_To_Move = [0] * 3
        Stp_To_Move[0] = self.custom_round(x_ToMove * (400 / 8))
        Stp_To_Move[1] = self.custom_round(y_ToMove * (400 / 8))
        Stp_To_Move[2] = self.custom_round(z_ToMove * (400 / 8))
        return Stp_To_Move


        return Stp_To_Move

    def calibrate_X(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving = 1
            self.send_to_arduino('CX')
            self.Status_textBrowser.append(datetime.now().strftime("[%H:%M:%S]: ") + "Calibrating X axis...")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def calibrate_Y(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving = 1
            self.send_to_arduino('CY')
            self.Status_textBrowser.append(datetime.now().strftime("[%H:%M:%S]: ") + "Calibrating Y axis...")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def calibrate_All(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving = 1
            self.send_to_arduino('CA')
            self.Status_textBrowser.append(datetime.now().strftime("[%H:%M:%S]: ") + "Calibrating All axis...")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def X_Home(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            x_coord_v = 0.000 
            y_coord_v = self.M_CurrentPos[1]

            x_ToMove = x_coord_v - self.M_CurrentPos[0]
            y_ToMove = y_coord_v - self.M_CurrentPos[1]

            self.M_CurrentPos[0] = x_coord_v
            self.M_CurrentPos[1] = y_coord_v

            # Generate the G-code command
            steps = self.calculate_steps_to_move(x_ToMove, y_ToMove, 0.0)
            gcode_send = "G0X{:0=+}".format(steps[0])
            gcode_display = "G0X{:0=+}".format(steps[0])
            # Send the G-code to Arduino 
            self.send_to_arduino(gcode_send)
            self.display_gcode(gcode_display)
            # Set line edit for current pos
            self.X_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[0]))
            self.Y_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[1]))
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def Y_Home(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            x_coord_v = self.M_CurrentPos[0]
            y_coord_v = 0.000

            x_ToMove = x_coord_v - self.M_CurrentPos[0]
            y_ToMove = y_coord_v - self.M_CurrentPos[1]

            self.M_CurrentPos[0] = x_coord_v
            self.M_CurrentPos[1] = y_coord_v

            # Generate the G-code command
            steps = self.calculate_steps_to_move(x_ToMove, y_ToMove, 0.0)
            gcode_send = "G0Y{:0=+}".format(steps[1])
            gcode_display = "G0Y{:0=+}".format(steps[1])
            # Send the G-code to Arduino 
            self.send_to_arduino(gcode_send)
            self.display_gcode(gcode_display)
            # Set line edit for current pos
            self.X_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[0]))
            self.Y_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[1]))
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def Home_All(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            # Get the values from the lineEdits
            x_coord_v = 0.000
            y_coord_v = 0.000 

            x_ToMove = x_coord_v - self.M_CurrentPos[0]
            y_ToMove = y_coord_v - float(self.M_CurrentPos[1])

            self.M_CurrentPos[0] = x_coord_v
            self.M_CurrentPos[1] = y_coord_v

            # Generate the G-code command
            steps = self.calculate_steps_to_move(x_ToMove, y_ToMove, 0.0)
            gcode_send = "G0X{:0=+}Y{:0=+}".format(steps[0], steps[1])
            gcode_display = "G0X{:0=+}Y{:0=+}".format(steps[0], steps[1])
            # Send the G-code to Arduino 
            self.send_to_arduino(gcode_send)
            self.display_gcode(gcode_display)

            # set line edit for current pos
            self.X_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[0]))
            self.Y_lineEdit.setText("{:.3f}".format(self.M_CurrentPos[1]))
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")
            
    def move_X_positive(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            if self.M_CurrentPos[0] < self.Machine_Max_UpperLim[0]:
                VAL = 0.0
                if self.Hundred_radioButton.isChecked():
                    VAL = 100
                elif self.Ten_radioButton.isChecked():
                    VAL = 10
                elif self.One_radioButton.isChecked():
                    VAL = 1
                elif self.DotOne_radioButton.isChecked():
                    VAL = 0.1
                else:
                    gcode_send = ""
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Please Check in check box")
                
                if  self.M_CurrentPos[0] + VAL >  self.Machine_Max_UpperLim[0]:
                    VAL = self.Machine_Max_UpperLim[0] - self.M_CurrentPos[0]
                    self.M_CurrentPos[0] = self.Machine_Max_UpperLim[0]
                else:
                    self.M_CurrentPos[0] = self.M_CurrentPos[0] + VAL

                self.X_lineEdit.setText("{:.1f}".format(float(self.M_CurrentPos[0])))
                gcode_send = "G0X{:0=+06.1f}".format(VAL*(400/8))
                gcode_display = "G0X{:0=+06.1f}".format(VAL)
                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_display)
                self.Disable_Function()
            else:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Unable to move, exceed axis limit!!!")
           
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def move_X_negative(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            if self.M_CurrentPos[0] >  self.Machine_Max_LowerLim[0]:
                VAL = 0.0
                if self.Hundred_radioButton.isChecked():
                    VAL = -100
                elif self.Ten_radioButton.isChecked():
                    VAL = -10
                elif self.One_radioButton.isChecked():
                    VAL = -1
                elif self.DotOne_radioButton.isChecked():
                    VAL = -0.1
                else:
                    gcode_send = ""
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Please Check in check box")
                
                if  self.M_CurrentPos[0] + VAL <  self.Machine_Max_LowerLim[0]:
                    VAL = self.Machine_Max_LowerLim[0] - self.M_CurrentPos[0]
                    self.M_CurrentPos[0] = self.Machine_Max_LowerLim[0]
                else:
                    self.M_CurrentPos[0] = self.M_CurrentPos[0] + VAL

                self.X_lineEdit.setText("{:.3f}".format(float(self.M_CurrentPos[0])))
                gcode_send = "G0X{:0=+}".format(VAL*(400/8))
                gcode_display = "G0X{:0=+}".format(VAL)
                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_display)
                self.Disable_Function()
            else:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Unable to move, exceed axis limit!!!")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def move_Y_positive(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            if self.M_CurrentPos[1] < self.Machine_Max_UpperLim[1]:
                VAL = 0.0
                if self.Hundred_radioButton.isChecked():
                    VAL = 100
                elif self.Ten_radioButton.isChecked():
                    VAL = 10
                elif self.One_radioButton.isChecked():
                    VAL = 1
                elif self.DotOne_radioButton.isChecked():
                    VAL = 0.1
                else:
                    gcode_send = ""
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Please Check in check box")
                
                if  self.M_CurrentPos[1] + VAL >  self.Machine_Max_UpperLim[1]:
                    VAL = self.Machine_Max_UpperLim[1] - self.M_CurrentPos[1]
                    self.M_CurrentPos[1] = self.Machine_Max_UpperLim[1]
                else:
                    self.M_CurrentPos[1] = self.M_CurrentPos[1] + VAL

                self.Y_lineEdit.setText("{:.1f}".format(float(self.M_CurrentPos[1])))
                gcode_send = "G0Y{:0=+06.1f}".format(VAL*(400/8))
                gcode_display = "G0Y{:0=+06.1f}".format(VAL)
                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_display)
                self.Disable_Function()
            else:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Unable to move, exceed axis limit!!!")  
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def move_Y_negative(self):
        if self.Connect_pushButton.text() == "Disconnect":
            self.IsMoving_1 = 1
            if self.M_CurrentPos[1] >  self.Machine_Max_LowerLim[1]:
                VAL = 0.0
                if self.Hundred_radioButton.isChecked():
                    VAL = -100
                elif self.Ten_radioButton.isChecked():
                    VAL = -10
                elif self.One_radioButton.isChecked():
                    VAL = -1
                elif self.DotOne_radioButton.isChecked():
                    VAL = -0.1
                else:
                    gcode_send = ""
                    current_time = datetime.now().strftime('%H:%M:%S')
                    self.Status_textBrowser.append(f"[{current_time}] Please Check in check box")
                
                if  self.M_CurrentPos[1] + VAL <  self.Machine_Max_LowerLim[1]:
                    VAL = self.Machine_Max_LowerLim[1] - self.M_CurrentPos[1]
                    self.M_CurrentPos[1] = self.Machine_Max_LowerLim[1]
                else:
                    self.M_CurrentPos[1] = self.M_CurrentPos[1] + VAL

                self.Y_lineEdit.setText("{:.3f}".format(float(self.M_CurrentPos[1])))
                gcode_send = "G0Y{:0=+}".format(int(VAL*(400/8)))
                gcode_display = "G0Y{:0=+}".format(VAL)
                self.send_to_arduino(gcode_send)
                self.display_gcode(gcode_display)
                self.Disable_Function()
            else:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser.append(f"[{current_time}] Unable to move, exceed axis limit!!!")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

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
    
    def display_gcode_2(self, gcode_command):
        if hasattr(self, 'ser') and self.ser.is_open:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.Status_textBrowser_2.append(f"[{current_time}] Sent: {gcode_command}")
            except Exception as e:
                self.Status_textBrowser_2.append(f"Error sending command: {e}")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser_2.append(f"[{current_time}] Arduino not connected")
        
    def update_speed_label(self):
        if self.Connect_pushButton.text() == "Disconnect":
            slider_value = self.Speed_horizontalSlider.value()  # Get the current slider value
            speeds = {
                1: (100, 100),
                2: (125, 125),
                3: (150, 150),
                4: (175, 175),
                5: (200, 200)
            }
            x_speed, y_speed, z_speed = speeds.get(slider_value, (100, 100))  # Default 
            current_time = datetime.now().strftime('%H:%M:%S')
            self.label_22.setText(f"{x_speed}, {y_speed}")
            self.Status_textBrowser.append(f"[{current_time}] Speed set at {x_speed}, {y_speed} (mm/min)")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")

    def update_speed_label1(self):
        if self.Connect_pushButton.text() == "Disconnect":
            slider_value = self.Speed_horizontalSlider.value()  # Get the current slider value
            speed_commands = {
                1: "S1",
                2: "S2",
                3: "S3",
                4: "S4",
                5: "S5"
            }
            speed_command = speed_commands.get(slider_value, "S1")  # Default to S1 if value not found
            self.send_speed_to_arduino(speed_command)

    def send_speed_to_arduino(self, speed_command):
        if hasattr(self, 'ser') and self.ser.is_open:
            try:
                self.ser.write(f"{speed_command}\n".encode())  # Convert to bytes and send
                print(speed_command)
            except Exception as e:
                self.Status_textBrowser.append(f"Error sending speed command: {e}")

    def update_accel_label(self):
        if self.Connect_pushButton.text() == "Disconnect":
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
        if self.Connect_pushButton.text() == "Disconnect":
            slider_value = self.Acceleration_horizontalSlider.value()  # Get the current slider value
            accel_commands = {
                1: "A1",
                2: "A2",
                3: "A3",
                4: "A4",
                5: "A5"
            }
            accel_command = accel_commands.get(slider_value, "A1")  # Default to A1 if value not found
            self.send_accel_to_arduino(accel_command)
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")
            
    def send_accel_to_arduino(self, accel_command):
        if self.Connect_pushButton.text() == "Disconnect":
            try:
                self.ser.write(f"{accel_command}\n".encode())  # Convert to bytes and send
                print(accel_command)
            except Exception as e:
                self.Status_textBrowser.append(f"Error sending acceleration command: {e}")

    def display_distance_message(self, distance):
        current_time = datetime.now().strftime('%H:%M:%S')
        self.Status_textBrowser.append(f"[{current_time}] Distance set at {distance} mm")

    def Disable_Function(self):
        self.tab.setEnabled(False)
        self.tab_2.setEnabled(False)

    def Enable_Function(self): 
        self.tab.setEnabled(True)
        self.tab_2.setEnabled(True)

    def plot_gcode_commands(self, gcode_commands):
        # Clear any existing plot on tab 2
        self.clear_plot_on_tab2()

        self.x_coords = []
        self.y_coords = []

        for command in gcode_commands:
            if command.startswith('G0') or command.startswith('G1'):
                # Extract X and Y coordinates
                x_start = command.find('X') + 1
                x_end = command.find('Y')
                y_start = command.find('Y') + 1
                y_end = command.find('Z') if 'Z' in command else len(command)

                # Check if X and Y coordinates are found and Z coordinate is not found
                if x_start != -1 and x_end != -1 and y_start != -1 and (y_end != -1 or 'Z' not in command):
                    try:
                        x = float(command[x_start:x_end])
                        y = float(command[y_start:y_end])

                        self.x_coords.append(x)
                        self.y_coords.append(y)
                    except ValueError:
                        continue

        # Create plot using Matplotlib
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.x_coords, self.y_coords, marker='o', linestyle='-', color='black', markersize=3)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('G-code Plot')
        self.ax.grid(True)
        self.fig.tight_layout()

        # Initialize the red '+' marker at the initial position
        if self.x_coords and self.y_coords:
            self.marker, = self.ax.plot(self.x_coords[0], self.y_coords[0], marker='+', color='red', markersize=20)

        # Create FigureCanvas and embed into the widget designed in Qt Creator
        canvas = FigureCanvas(self.fig)
        layout = self.widget.layout()  # Get the current layout of self.widget

        if layout is None:
            layout = QtWidgets.QVBoxLayout(self.widget)
            self.widget.setLayout(layout)
        else:
            # Clear the layout and its widgets
            self.clear_layout(layout)

        layout.addWidget(canvas)

    def clear_plot_on_tab2(self):
        # Clear plot on tab 2 by removing the canvas widget
        layout = self.widget.layout()
        if layout:
            self.clear_layout(layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def frame(self):
        if not self.x_coords or not self.y_coords:
            return

        self.rect_lines = []

        x_min, x_max = min(self.x_coords), max(self.x_coords)
        y_min, y_max = min(self.y_coords), max(self.y_coords)
      

        # Coordinates of the rectangle edges
        self.rect_coords = [
            ((x_min, y_min), (x_min, y_max)),   # Left edge
            ((x_min, y_max), (x_max, y_max)),   # Top edge
            ((x_max, y_max), (x_max, y_min)),   # Right edge
            ((x_max, y_min), (x_min, y_min))    # Bottom edge
        ]
        for i in  self.rect_coords:
            print("line", i)
        # Start drawing the rectangle edges one by one
        self.edge_index = 0
        self.timer = QTimer()
        self.Is_Move_Frame = 1
        self.draw_next_edge()
        self.Disable_Function()
        #self.timer.timeout.connect(self.draw_next_edge)
        #self.timer.start(500)  # Draw each edge every second

    def draw_next_edge(self):
        if self.Connect_pushButton.text() == "Disconnect":
            start, end = self.rect_coords[self.edge_index]
            line, = self.ax.plot([start[0], end[0]], [start[1], end[1]], 'r-')
            print("Point 1:" + str(start[0]) + "," + str(end[0]))
            print("Point 2:" + str(start[1]) + "," + str(end[1]))
            self.rect_lines.append(line)
            self.fig.canvas.draw_idle()
            self.edge_index += 1
            steps = self.calculate_steps_to_move(end[0], end[1], 0.0)
            gcode_send = "G0X{:0=+}Y{:0=+}".format(steps[0] + self.displacement[0] - self.M_CurrentPos[0], steps[1] + self.displacement[1] - self.M_CurrentPos[1])
            self.M_CurrentPos[0] = steps[0]
            self.M_CurrentPos[1] = steps[1]
            gcode_display = "G0X{:0=+}Y{:0=+}".format(steps[0], steps[1])
            # Send the G-code to Arduino 
            self.send_to_arduino(gcode_send)
            self.display_gcode_2(gcode_display)
            self.Disable_Function()
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            self.Status_textBrowser.append(f"[{current_time}] Arduino not connected")
            # tao bien current position moi(chi de plot thoi)
    def remove_frame(self):
        for line in self.rect_lines:
            line.remove()
        self.rect_lines = []
        self.fig.canvas.draw_idle()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


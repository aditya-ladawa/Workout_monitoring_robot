from PySide6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 550)
        MainWindow.setStyleSheet("QMainWindow{\n"
"background-color: rgb(0, 255, 255);\n"
"\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.curls = QtWidgets.QPushButton(self.centralwidget)
        self.curls.setGeometry(QtCore.QRect(60, 130, 171, 51))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(QtGui.QFont.Normal)
        self.curls.setFont(font)
        self.curls.setStyleSheet("background-color: rgb(135, 135, 135);\n"
"color: rgb(255, 255, 255);\n"
"font: 13pt \"MS Shell Dlg 2\";")
        self.curls.setObjectName("curls")
        self.pushup = QtWidgets.QPushButton(self.centralwidget)
        self.pushup.setGeometry(QtCore.QRect(60, 290, 171, 51))
        self.pushup.setStyleSheet("background-color: rgb(135, 135, 135);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"MS Shell Dlg 2\";")
        self.pushup.setObjectName("pushup")
        self.view = QtWidgets.QLabel(self.centralwidget)
        self.view.setGeometry(QtCore.QRect(270, 130, 600, 450))
        self.view.setStyleSheet("background-color: rgb(157, 157, 157);")
        self.view.setText("")
        self.view.setObjectName("view")
        self.squats = QtWidgets.QPushButton(self.centralwidget)
        self.squats.setGeometry(QtCore.QRect(60, 370, 171, 51))
        self.squats.setStyleSheet("background-color: rgb(135, 135, 135);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"MS Shell Dlg 2\";")
        self.squats.setObjectName("squats")
        self.back = QtWidgets.QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(60, 490, 171, 51))
        self.back.setStyleSheet("background-color: rgb(135, 135, 135);\n"
"color: rgb(255, 255, 255);\n"
"font: 15pt \"MS Shell Dlg 2\";")
        self.back.setObjectName("back")
        self.information = QtWidgets.QLabel(self.centralwidget)
        self.information.setGeometry(QtCore.QRect(890, 130, 261, 241))
        self.information.setStyleSheet("background-color: rgb(157, 157, 157);")
        self.information.setText("")
        self.information.setObjectName("information")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(1030, 450, 111, 91))
        self.lcdNumber.setDigitCount(2)
        self.lcdNumber.setObjectName("lcdNumber")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(870, 470, 121, 61))
        self.label_2.setStyleSheet("border-color: rgb(255, 170, 0);\n"
"font: 45 48pt \"Calibri\";\n"
"color: rgb(255, 255, 255);\n"
"font:30pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(890, 390, 91, 51))
        self.stop.setStyleSheet("background-color: rgb(135, 135, 135);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.stop.setObjectName("stop")
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setGeometry(QtCore.QRect(1020, 380, 121, 61))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(25)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(QtGui.QFont.Normal)
        self.timeLabel.setFont(font)
        self.timeLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.timeLabel.setObjectName("timeLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1173, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.curls.setText(_translate("MainWindow", " BARBELL CURLS"))
        self.pushup.setText(_translate("MainWindow", "PUSHUP"))
        self.squats.setText(_translate("MainWindow", "SQUATS"))
        self.back.setText(_translate("MainWindow", "BACK"))
        self.label_2.setText(_translate("MainWindow", " REP"))
        self.stop.setText(_translate("MainWindow", "STOP"))
        self.timeLabel.setText(_translate("MainWindow", "00:00"))

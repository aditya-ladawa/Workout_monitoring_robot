from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

# app = QApplication(sys.argv)
# MainWindow = QMainWindow()
# MainWindow.setFixedSize(1173, 609)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1173, 609)
        MainWindow.setMouseTracking(False)
        MainWindow.setStyleSheet("QMainWindow{\n"

"background-color: rgb(0, 255, 255);\n"
"background-image: url(./images/bg_transparent.jpg);\n"
"background-position: center;\n"
"\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.uName = QtWidgets.QLabel(self.centralwidget)
        self.uName.setGeometry(450, 90, 291, 71)
        self.uName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.uName.autoFillBackground()
        self.uName.setStyleSheet(
"color: rgb(255, 255, 255);\n"
"font: 18pt \"MS Shell Dlg 2\";")
        self.uName.setObjectName('uName')
        self.dashboardButton = QtWidgets.QPushButton(self.centralwidget)
        self.dashboardButton.setGeometry(QtCore.QRect(450, 210, 291, 71))
        self.dashboardButton.setIcon(QtGui.QIcon('./images/dashboard.png'))
        self.dashboardButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.dashboardButton.setIconSize(QtCore.QSize(48,48))
        self.dashboardButton.setStyleSheet("background-color: #FB5B21;\n"
"color: rgb(255, 255, 255);\n"
"font: 20pt \"MS Shell Dlg 2\";"
"border-width: 5px;"
"border-radius: 10px;")
        self.dashboardButton.setObjectName("dashboardButton")
        self.exerciseButton = QtWidgets.QPushButton(self.centralwidget)
        self.exerciseButton.setGeometry(QtCore.QRect(450, 330, 291, 71))
        self.exerciseButton.setIcon(QtGui.QIcon('./images/u-1.png'))
        self.exerciseButton.setIconSize(QtCore.QSize(24,24))
        self.exerciseButton.setStyleSheet("background-color: #FB5B21;\n"
"color: rgb(255, 255, 255);\n"
"font: 20pt \"MS Shell Dlg 2\";")
        self.exerciseButton.setObjectName("exerciseButton")
        self.tutorialButton = QtWidgets.QPushButton(self.centralwidget)
        self.tutorialButton.setGeometry(QtCore.QRect(450, 450, 291, 71))
        self.tutorialButton.setStyleSheet("background-color: #FB5B21;\n"
"color: rgb(255, 255, 255);\n"
"font: 20pt \"MS Shell Dlg 2\";")
        self.tutorialButton.setObjectName("tutorialButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.uName.setText(_translate("MainWindow", "User_Name"))
        self.dashboardButton.setText(_translate("MainWindow", "Dashboard"))
        self.exerciseButton.setText(_translate("MainWindow", "Monitor Exercise"))
        self.tutorialButton.setText(_translate("MainWindow", "Tutorial"))

# def homeUi():
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     ui.uName.setText(f'Welcome, home!')
#     #ui.dashboardButton.clicked.connect(dashboardUi)
#     #ui.exerciseButton.clicked.connect(tutorialUi)
#     #ui.tutorialButton.clicked.connect(exerciseUi)
#     MainWindow.show()

# homeUi()

# sys.exit(app.exec())
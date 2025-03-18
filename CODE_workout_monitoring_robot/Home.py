from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QApplication, QMainWindow
from PySide6.QtGui import QIcon
import sys

from Tutorial import Tutorial
from Dashboard import Dashboard
from Exercise import Exercise

from home import Ui_MainWindow

class Home(QMainWindow, Ui_MainWindow):
    def __init__(self, welcome_window, username):
        super().__init__()
        self.setupUi(self)  # Setup the UI from Ui_MainWindow
        self.setWindowTitle("Home")
        self.setFixedSize(1173, 609)
        self.username = username
        self.welcome_window = welcome_window
        self.welcome_window.communicate.dashboard_signal.connect(self.open_dashboard)
        self.welcome_window.communicate.exercise_signal.connect(self.open_exercise)
        self.welcome_window.communicate.tutorial_signal.connect(self.open_tutorial)
        self.welcome_window.communicate.home_signal.connect(self.back_to_home)
        self.sc_count = 0

        # Display username
        self.uName.setText(f"User Name: {self.username}")

        # Connect button signals to slots
        self.dashboardButton.clicked.connect(self.open_dashboard)
        self.tutorialButton.clicked.connect(self.open_tutorial)
        self.exerciseButton.clicked.connect(self.open_exercise)

    def open_dashboard(self):
        if self.sc_count == 0:
            self.sc_count = 1
            self.hide()
            self.dashboard_window = Dashboard(self, self.username)
            self.dashboard_window.show()

    def open_exercise(self):
        if self.sc_count == 0:
            self.sc_count = 2
            self.hide()
            self.exercise_window = Exercise(self, self.username)
            self.exercise_window.show()

    def open_tutorial(self):
        if self.sc_count == 0:
            self.sc_count = 3
            self.hide()
            self.tutorial_window = Tutorial(self, self.username)
            self.tutorial_window.show()

    def back_to_home(self):
        if self.sc_count == 2:
            if hasattr(self, 'exercise_window'):
                self.sc_count = 0
                self.exercise_window.close()
            self.show()
        elif self.sc_count == 1:
            if hasattr(self, 'dashboard_window'):
                self.sc_count = 0
                self.dashboard_window.close()
            self.show()
        elif self.sc_count == 3:
            if hasattr(self, 'tutorial_window'):
                self.sc_count = 0
                self.tutorial_window.close()
            self.show()

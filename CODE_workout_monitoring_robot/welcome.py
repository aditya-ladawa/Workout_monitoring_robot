from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.centralwidget = QWidget(MainWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.label = QLabel(self.centralwidget)
        self.movie = QMovie('REEE.gif')
        self.label.setMovie(self.movie)
        self.verticalLayout.addWidget(self.label)
        self.movie.start()
        MainWindow.setCentralWidget(self.centralwidget)
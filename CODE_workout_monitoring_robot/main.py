import subprocess
import sys
import threading
from PySide6.QtCore import Signal, QObject, Qt, QTimer
from PySide6.QtGui import QMovie, QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton
from Dashboard import Dashboard
from Exercise import Exercise
from Home import Home
from Tutorial import Tutorial
import speech_recognition as sr
import cv2
from f_rec import f_rec

class Communicate(QObject):
    hello_signal = Signal()
    monitor_signal = Signal()
    stop_monitoring_signal = Signal()
    dashboard_signal = Signal()
    tutorial_signal = Signal()
    exercise_signal = Signal()
    home_signal = Signal()


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setFixedSize(900, 550)
        self.communicate = Communicate()
        self.recognizer = sr.Recognizer()
        self.userName = 'UserName'
        self.listening_thread = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Load GIF
        self.gif_path = "REEE.gif"
        self.movie = QMovie(self.gif_path)

        # Display GIF
        self.gif_label = QLabel()
        self.gif_label.setMovie(self.movie)
        layout.addWidget(self.gif_label)

        # Start the animation
        self.movie.start()

        # Connect signals to slots
        self.communicate.hello_signal.connect(self.on_hello)
        # self.communicate.monitor_signal.connect(self.on_monitor)
        # self.communicate.stop_monitoring_signal.connect(self.on_stop_monitoring)
        # self.communicate.hello_signal.emit()

    def start_listening(self):
        # while True:
        #     ch = int(input())
        #     if ch == 0:
        #         self.communicate.hello_signal.emit()
        #     elif ch == 1:
        #         self.communicate.dashboard_signal.emit()
        #     elif ch == 2:
        #         self.communicate.exercise_signal.emit()
        #     elif ch == 4:
        #         self.communicate.home_signal.emit()

        with sr.Microphone() as source:
            while True:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio)
                    print("You said:"+text)
                    if  "robot" in text.lower():
                        self.communicate.hello_signal.emit()
                    elif "monitor exercise" in text.lower():
                        self.communicate.monitor_signal.emit()
                    elif "stop monitoring" in text.lower():
                        self.communicate.stop_monitoring_signal.emit()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results")

    def on_hello(self):
        frc = f_rec()
        val = frc.recognize_face()
        
        if(val[0] == 1):
            self.userName = val[1]
            text = 'Welcome' + self.userName
            self.speak(text)
            self.hide()
            self.home = Home(self, self.userName)
            self.home.show()

        elif(val[0] == 0):
            self.ask_user_for_name()
            frc.capture_and_encode(self.userName)
            text = 'Welcome' + self.userName

            self.speak(text)
            self.hide()
            self.home = Home(self, self.userName)
            self.home.show()
        
    def speak(self, text):
        subprocess.getstatusoutput(f'espeak -v en-us+f3 -s150 {text}')

    def ask_user_for_name(self):
        recognizer = sr.Recognizer()
        flag = 1
        while flag == 1:
            with sr.Microphone() as source:
                text = "please,say your name"
                self.speak(text)
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            try:
                user_name = recognizer.recognize_google(audio).capitalize()
                txt = "your name is set as,"+user_name
                self.speak(txt)
                flag = 0
                self.userName = user_name
                break
            except sr.UnknownValueError:
                self.speak("Sorry, could not understand audio.")
                flag = 1
            except sr.RequestError as e:
                self.speak("Could not request results")
                flag = 1

    def on_dashboard(self):
        if self.home:
            if self.home.sc_count==0:
                self.home.sc_count=1
                self.home.open_dashboard()
    
    def on_exercise(self):
        if self.home:
            if self.home.sc_count==0:
                self.home.sc_count=2
                self.home.open_exercise()
    
    def on_tutorial(self):
        if self.home:
            if self.home.sc_count==0:
                self.home.sc_count=3
                self.home.open_tutorial()

    def on_home(self):
        if self.home:
            if self.home.sc_count > 0:
                self.home.open_home()

    # def on_monitor(self):
    #     if self.dashboard_window:
    #         if self.dashboard_window.monitor_flag==0:
    #             self.dashboard_window.start_monitoring()

    # def on_stop_monitoring(self):
    #     if self.dashboard_window:
    #         if self.dashboard_window.monitor_flag==1:
    #             self.dashboard_window.stop_monitoring()

    def closeEvent(self, event):
        if self.listening_thread:
            self.listening_thread.stopped = True
            self.listening_thread.join()
            self.listening_thread = None
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    welcome_window.listening_thread = threading.Thread(target=welcome_window.start_listening)
    welcome_window.listening_thread.start()
    sys.exit(app.exec())

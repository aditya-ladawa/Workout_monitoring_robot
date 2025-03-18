from PySide6.QtCore import Signal, QObject, Qt, QTimer
from PySide6.QtGui import QMovie, QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton
import os
import json

class Tutorial(QMainWindow):
    def __init__(self, welcome_window, username):
        super().__init__()
        self.setWindowTitle("Tutorial")
        self.setFixedSize(1080, 600)
        self.username = username
        self.welcome_window = welcome_window

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Display username
        self.username_label = QLabel(f"User Name: {self.username}")
        layout.addWidget(self.username_label)



        # Start monitoring button
        self.monitor_button = QPushButton("Monitor Exercise")
        self.monitor_button.clicked.connect(self.start_monitoring)
        layout.addWidget(self.monitor_button)

        # Stop monitoring button
        self.stop_monitoring_button = QPushButton("User Dashboard")
        self.stop_monitoring_button.clicked.connect(self.stop_monitoring)
        layout.addWidget(self.stop_monitoring_button)

        # Start follow button
        self.start_follow = QPushButton("Tutorial")
        self.start_follow.clicked.connect(self.hfl.start_follow)
        layout.addWidget(self.start_follow)


        # Timer for video update
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_video)

    def start_monitoring(self):
        if self.monitor_flag == 0:
            pass

    def stop_monitoring(self):
        if self.monitor_flag == 1:
            if self.video_thread:
                self.video_thread.stop()
                self.video_thread = None
                self.video_timer.stop()  # Stop timer for updating video
                self.video_label.clear()  # Clear video display
                self.clear_records()  # Clear record tables
                print("Monitoring stopped")
                self.monitor_flag=0

    def update_video(self):
        if self.video_thread:
            frame = self.video_thread.get_frame()
            if frame is not None:
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.video_label.setPixmap(pixmap)

    def show_records(self):
        date = self.calendar.selectedDate().toString(Qt.ISODate)
        if date in self.calendar_records:
            record_table = self.calendar_records[date]
            record_table.show()
        else:
            self.load_records(date)

    def load_records(self, date):
        records = self.fetch_records(date)
        if records:
            table = QTableWidget()
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Exercise Name", "Sets", "Errors"])
            table.setRowCount(len(records))
            for i, record in enumerate(records):
                table.setItem(i, 0, QTableWidgetItem(record["exercise_id"]))
                table.setItem(i, 1, QTableWidgetItem(str(record["repetition"])))
                # Format errors
                errors = ", ".join([f"{key}: {value}" for error in record["errors"] for key, value in error.items()])
                table.setItem(i, 2, QTableWidgetItem(errors))
            self.calendar_records[date] = table
            table.show()

    def fetch_records(self, date):
        records = []
        filename = os.path.join("exercise_data", f"{date}.json")
        if os.path.exists(filename):
            with open(filename, "r") as file:
                records = json.load(file)
        return records

    def clear_records(self):
        for table in self.calendar_records.values():
            table.hide()
            table.deleteLater()
        self.calendar_records = {}
    
    def follow_human(self):
        self.hfl.follow()
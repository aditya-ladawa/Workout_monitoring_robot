from PySide6.QtCore import Signal, QObject, Qt, QTimer, QTime
from PySide6.QtGui import QMovie, QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton
import cv2
import countcopy
from ex_final_ import *
import subprocess

class Exercise(QMainWindow, countcopy.Ui_MainWindow):
    def __init__(self, home_window, username):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Exercise")
        # self.setFixedSize(1080, 600)

        self.username = username
        self.home_window = home_window
        self.previous_q_values = [0] * 6  # Initialize with None for comparison
        self.q_names = ["PCR", "LUAR", "PCL", "LUAL", "LBE", "Rep"]  # Names for the metrics
        self.start_time = None
        self.elapsed_time = QTime(0, 0, 0)


        self.back.clicked.connect(self.home_window.back_to_home)
        self.curls.clicked.connect(self.monitor_curls)
        self.stop.clicked.connect(self.stop_monitoring)
        self.home_window.welcome_window.communicate.monitor_signal.connect(self.monitor_curls)
        self.home_window.welcome_window.communicate.stop_monitoring_signal.connect(self.stop_monitoring)

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time_label)

        self.cap = cv2.VideoCapture(0)

        # Timer for video update
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_video)
        
    def monitor_curls(self):
        # Start the video timer to update video feed
        self.video_timer.start(10) 

        self.start_time = QTime.currentTime()
        self.time_timer.start(1000)
    
    def update_video(self):
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)

            if ret:
                # Perform analysis on the frame here
                image, results = mediapipe_detection(frame, pose)
                
                if results.pose_landmarks:
                    draw_landmarks(image, results)
                    keypoints = extract_keypoints(results)
                    q = analyze_bicep_curls(image, results)
                    for i, (prev, curr) in enumerate(zip(self.previous_q_values, q[:6])):
                        if prev != curr:
                            print(f"{self.q_names[i]}: {curr}")
                            text = 'error'+self.q_names[i]+str(curr)
                            subprocess.getstatusoutput(f'espeak -v en-us+f3 -s150 {text}')
                            self.previous_q_values[i] = curr
                    self.update_rep(q[5])
                # Convert the image to display in QLabel
                h, w, c = image.shape
                bytes_per_line = c * w
                # Resize the image
                resized_image = cv2.resize(image, (640, 480))
                # Convert to RGB888 format
                rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
                # Create QImage
                convert_to_Qt_format = QImage(rgb_image.data, 640, 480, bytes_per_line, QImage.Format_RGB888)
                pix = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.view.setPixmap(QPixmap.fromImage(pix))

    def stop_monitoring(self):
        # Stop the video timer
        self.video_timer.stop()

        self.time_timer.stop()

        # Reset elapsed time
        self.elapsed_time = QTime(0, 0, 0)
        self.update_time_label()

    def closeEvent(self, event):
        # Release the VideoCapture object
        if self.cap.isOpened():
            self.stop_monitoring
            self.cap.release()
        event.accept()
    
    def update_rep(self, rep):
        self.lcdNumber.display(rep)

    def update_time_label(self):
        if self.start_time is not None:
            # Calculate elapsed time
            elapsed_seconds = self.start_time.secsTo(QTime.currentTime())
            elapsed_minutes = elapsed_seconds // 60
            elapsed_seconds %= 60
            # Update time label with elapsed time
            self.timeLabel.setText(f"{elapsed_minutes:02d}:{elapsed_seconds:02d}")
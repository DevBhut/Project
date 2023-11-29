import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from posture import PostureWatcher
import threading

class Application(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Posture Watcher")
        self.pw = PostureWatcher()
        self.base_posture_set = False

        self.layout = QVBoxLayout()

        # Set base posture button
        self.set_base_button = QPushButton("Set base posture")
        self.set_base_button.clicked.connect(self.set_base_posture)
        self.layout.addWidget(self.set_base_button)

        # Clear base posture button
        self.clear_base_button = QPushButton("Clear base posture")
        self.clear_base_button.clicked.connect(self.clear_base_posture)
        self.layout.addWidget(self.clear_base_button)

        # Quit button
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit)
        self.layout.addWidget(self.quit_button)

        # Posture status label
        self.posture_label = QLabel("⚠️ Please set your base posture.")
        self.layout.addWidget(self.posture_label)

        # Create a widget to display camera feed
        self.video_widget = QLabel()
        self.layout.addWidget(self.video_widget)

        # Create a timer for updating the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(30)  # Adjust the update interval as needed

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Create a thread for posture checking
        self.posture_thread = threading.Thread(target=self.check_posture)
        self.posture_thread.daemon = True
        self.posture_thread.start()

    def set_base_posture(self):
        self.pw.set_base_posture()
        self.base_posture_set = True

    def clear_base_posture(self):
        self.pw.base_posture = None
        self.base_posture_set = False

    def quit(self):
        self.pw.stop()
        self.close()

    def check_posture(self):
        while True:
            self.pw.run()

    def update_title(self):
        if not self.base_posture_set:
            self.posture_label.setText("⚠️ Please set your base posture.")
        else:
            cd = self.pw.deviation.current_deviation
            if cd < 25:
                self.posture_label.setText("Posture Watcher: ✅ Great posture!")
            elif cd < 35:
                self.posture_label.setText(f"Posture Watcher: ⚠️ Improve your posture! ({cd}%)")
            else:
                self.posture_label.setText(f"Posture Watcher: ⛔️ Fix your posture! ({cd}%)")

    def update_camera_feed(self):
        ret, frame = self.pw.get_camera_frame()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_widget.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()

    # Create a thread for title updates
    title_thread = threading.Thread(target=window.update_title)
    title_thread.daemon = True
    title_thread.start()

    sys.exit(app.exec_())
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl
from PyQt6 import uic

import Mozaik
import compare

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        self.load_ui()

        # Set window title
        self.setWindowTitle('Image Comparator')

        # Find buttons in UI
        self.button1 = self.findChild(QPushButton, 'pushButton')
        self.button2 = self.findChild(QPushButton, 'pushButton_2')

        # Connect buttons to functions
        self.button1.clicked.connect(self.run_program1)
        self.button2.clicked.connect(self.run_program2)

        # Initialize Mozaik and Compare programs
        self.mozaik_program = None
        self.compare_program = None

        # Set default image paths
        self.path1 = "Fire.png"
        self.path2 = "Water.png"

        # Set up background image
        self.set_background_image("tlomenu.gif")

        # Set up background music
        self.setup_background_music()

    def load_ui(self):
        # Load UI from the file
        uic.loadUi('menu.ui', self)

    def set_background_image(self, gif_path):
        movie = QMovie(gif_path)
        movie.setScaledSize(self.size())  # Resize the movie to fit the window
        label = QLabel(self)
        label.setMovie(movie)
        movie.start()

        # Set the label geometry to cover the entire window
        label.setGeometry(0, 0, self.width(), self.height())

        # Move the label to the bottom layer
        label.lower()

    def setup_background_music(self):
        print("Setting up background music...")

        # Initialize QMediaPlayer and QMediaPlaylist for background music
        self.background_music_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.background_music_player.setAudioOutput(self.audio_output)

        music_file_path = "bg_music.mp3"
        print(f"Attempting to load music from: {music_file_path}")

        self.background_music_player.setSource(QUrl.fromLocalFile(music_file_path))

        if self.background_music_player.isAvailable():
            print("Background music is available.")
        else:
            print("Background music is NOT available.")

        self.audio_output.setVolume(50)
        self.background_music_player.play()
        print("Background music setup complete.")

    def run_program2(self):
        # Stop background music when running compare program
        # self.background_music_player.stop()

        self.compare_program = compare.ImageComparator(self.path1, self.path2)
        self.compare_program.showFullScreen()

    def run_program1(self):
        # Stop background music when running mozaik program
        # self.background_music_player.stop()

        self.mozaik_program = Mozaik.Mozaik(self.path1, self.path2)
        self.mozaik_program.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec())

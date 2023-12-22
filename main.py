import Mozaik
import compare
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,QFileDialog
from PyQt6.QtGui import QMovie
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl
from PyQt6 import uic
from PyQt6.QtCore import Qt


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.setWindowTitle('Image Comparator')

        toolbar = self.addToolBar("Menu")
        toolbar2 = self.addToolBar("Menu")
        self.Image1PathName = QLabel("Image 1")
        self.Image2PathName = QLabel("Image 2")
        toolbar.addWidget(self.Image1PathName)
        toolbar2.addWidget(self.Image2PathName)

        self.button1 = self.findChild(QPushButton, 'pushButton')
        self.button2 = self.findChild(QPushButton, 'pushButton_2')
        self.ImageSelectButton = self.findChild(QPushButton, 'ImageSelect')
        self.ImageSelectButton2 = self.findChild(QPushButton, 'ImageSelect2')


        self.button1.clicked.connect(self.run_program1)
        self.button2.clicked.connect(self.run_program2)
        self.ImageSelectButton.clicked.connect(self.OpenFile1)
        self.ImageSelectButton2.clicked.connect(self.OpenFile2)

        self.mozaik_program = None
        self.compare_program = None

        self.path1 = "Fire.png"
        self.path2 = "Water.png"

        self.Image1PathName.setText(f"File Path 1: {self.path1}")
        self.Image2PathName.setText(f"File Path 2: {self.path2}")

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
        self.compare_program = compare.ImageComparator(self.path1, self.path2)
        self.compare_program.showFullScreen()

    def run_program1(self):
        self.mozaik_program = Mozaik.Mozaik(self.path1, self.path2)
        self.mozaik_program.showFullScreen()

    def OpenFile1(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Image File")
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp *.gif)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            #print("ImageAccepted")
            selected_file = file_dialog.selectedFiles()[0]
            #print(selected_file)
            self.path1 = selected_file;
            self.Image1PathName.setText(f"File Path 1: {selected_file}")



    def OpenFile2(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Image File")
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp *.gif)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            # print("ImageAccepted")
            selected_file = file_dialog.selectedFiles()[0]
            # print(selected_file)
            self.path2 = selected_file;
            self.Image2PathName.setText(f"File Path 12: {selected_file}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec())
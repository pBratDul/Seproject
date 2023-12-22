from PyQt6.QtGui import QPixmap

import Mozaik
import compare
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt6 import uic
from PyQt6.QtCore import Qt


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.setWindowTitle('Image Comparator')

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

        border_image_path = "tlomenu.jpg"
        self.setStyleSheet(f"QMainWindow {{ border-image: url({border_image_path}); }}")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec())
import Mozaik
import compare
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6 import uic

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.setWindowTitle('Image Comparator')
        self.button1 = self.findChild(QPushButton, 'pushButton')
        self.button2 = self.findChild(QPushButton, 'pushButton_2')

        self.button1.clicked.connect(self.run_program1)
        self.button2.clicked.connect(self.run_program2)

        
        self.mozaik_program = None  
        self.compare_program = None

        self.path1 = "Fire.png"
        self.path2 = "Water.png"

    def run_program2(self):
        self.compare_program = compare.ImageComparator(self.path1, self.path2)

        self.compare_program.showFullScreen()

    def run_program1(self):
        self.mozaik_program = Mozaik.Mozaik(self.path1, self.path2)
        
           

        self.mozaik_program.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec())

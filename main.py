import Mozaik
import compare
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6 import uic

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('C:\\Users\\kubaz\\Desktop\\Seproject-Mozaik\\Seproject-Mozaik\\menu.ui', self)

        self.button1 = self.findChild(QPushButton, 'pushButton')
        self.button2 = self.findChild(QPushButton, 'pushButton_2')

        self.button1.clicked.connect(self.run_program1)
        self.button2.clicked.connect(self.run_program2)

        
        self.mozaik_program = None  
        self.compare_program = None  

    def run_program2(self):
        path1 = "C:\\Users\\kubaz\\Desktop\\Seproject-Mozaik\\Seproject-Mozaik\\B1.png"
        path2 = "C:\\Users\\kubaz\\Desktop\\Seproject-Mozaik\\Seproject-Mozaik\\C2.png"

       
        self.compare_program = compare.ImageComparator(path1, path2)
       

        self.compare_program.showFullScreen()

    def run_program1(self):
        path1 = "C:\\Users\\kubaz\Desktop\\Seproject-Mozaik\\Seproject-Mozaik\\Fire.png"
        path2 = "C:\\Users\\kubaz\Desktop\\Seproject-Mozaik\\Seproject-Mozaik\\Water.png"

        
        self.mozaik_program = Mozaik.Mozaik(path1, path2)
        
           

        self.mozaik_program.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec())

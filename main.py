import sys

import Mozaik
import compare
from PyQt6.QtWidgets import QApplication
if __name__ == "__main__":

    # Żeby łatwo testować, twórzcie własny elif poniżej ze zmienną 'what_to_test'
    what_to_test = "mozaik"
    # what_to_test = "nic"

    if what_to_test == "slider_compare":
        app = QApplication(sys.argv)

        #path1 = "test_images/imgset0000/QM008.png"
        #path2 = "test_images/imgset0000/QM010.png"

        path1 = "B1.png"
        path2 = "C2.png"

        #path1 = "C1.png"
        #path2 = "C2.png"

        window = compare.ImageComparator(path1, path2)
        window.showFullScreen()

        sys.exit(app.exec())

    elif what_to_test == "nic":
        print("tets")


    elif what_to_test == "mozaik":
        app = QApplication(sys.argv)
        path1 = "Fire.png"
        path2 = "Water.png"

        window = Mozaik.Mozaik(path1, path2)
        window.showFullScreen()

        sys.exit(app.exec())

    else:
        print("Stwórz własny elif, który będzie odpowiadał za odpalenie Twojego kodu, "
              "następnie wpisz wymagany string w zmiennej 'what_to_test', "
              "żeby warunek był spełniony")

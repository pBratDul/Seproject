import compare
import tkinter as tk

if __name__ == "__main__":
    #path1 = "Kuba.jpg"
    #path2 = "Łukasz.jpg"

    path1 = "test_images/imgset0000/QM008.png"
    path2 = "test_images/imgset0000/QM010.png"

    #path1 = "test_images/imgset0594/LR000.png"
    #path2 = "test_images/imgset0594/LR001.png"

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    app = compare.ImageComparator(root, path1, path2)
    root.mainloop()
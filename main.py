import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class ImageComparator:
    def __init__(self, root, image1_path, image2_path):
        self.root = root
        self.root.title("Image Comparator")

        # Load images
        self.image1 = Image.open(image1_path)
        self.image2 = Image.open(image2_path)

        # Set initial zoom factor
        #self.zoom_factor = 1.0

        # Calculate initial zoom factor to fit the entire image within the window
        window_width = root.winfo_screenwidth()
        window_height = root.winfo_screenheight()
        initial_zoom_factor = min(window_width / self.image1.width, window_height / self.image1.height)
        self.zoom_factor = initial_zoom_factor

        # Variables for dragging
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Create canvas for image display
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create compare slider
        self.compare_slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_comparison)
        self.compare_slider.set(50)
        self.compare_slider.pack(pady=10)

        # Bind mouse events for dragging and zooming
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.zoom_image)

        # Bind slider motion to update the display smoothly
        self.compare_slider.bind("<Motion>", self.on_slider_motion)

        # Display initial images
        self.display_images()

    def display_images(self):
        # Resize images based on zoom factor
        width = int(self.image1.width * self.zoom_factor)
        height = int(self.image1.height * self.zoom_factor)

        resized_image1 = self.image1.resize((width, height), Image.BILINEAR)
        resized_image2 = self.image2.resize((width, height), Image.BILINEAR)

        # Get the separation position from the slider
        position = self.compare_slider.get() / 100.0

        # Calculate the separation point
        separation_point = int(position * width)

        # Create two images, one for the left side and one for the right side of the separation point
        left_image = resized_image1.crop((0, 0, separation_point, height))
        right_image = resized_image2.crop((separation_point, 0, width, height))

        # Create a composite image by overlaying the second image on top of the first one
        composite_image = Image.new("RGB", (width, height))
        composite_image.paste(left_image, (0, 0))
        composite_image.paste(right_image, (separation_point, 0))

        # Display the composite image on the canvas
        self.tk_composite_image = ImageTk.PhotoImage(composite_image)

        # Delete existing images on the canvas
        self.canvas.delete("composite_image")

        # Create the composite image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_composite_image, tags="composite_image")

    def update_comparison(self, event):
        # Update image comparison based on slider position
        position = self.compare_slider.get() / 100.0

        # Calculate the separation point based on the image width
        separation_point = int(position * self.image1.width * self.zoom_factor)

        self.canvas.delete("comparison_line")
        self.canvas.create_line(separation_point, 0,
                                separation_point, self.canvas.winfo_height(),
                                fill="red", tags="comparison_line")

    def on_press(self, event):
        # Mark the starting point for dragging
        self.canvas.scan_mark(event.x, event.y)

    def on_drag(self, event):
        # Drag images on canvas based on the current cursor position
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.display_images()

    def zoom_image(self, event):
        # Zoom in or out based on the mouse wheel movement
        factor = 1.2 if event.delta > 0 else 0.8
        self.zoom_factor *= factor
        self.display_images()

    def on_slider_motion(self, event):
        # Update the display smoothly when moving the slider
        self.root.after(1, self.display_images)


if __name__ == "__main__":
    # Replace 'image1.png' and 'image2.png' with the paths to your images
    #path1 = "Kuba.jpg"
    #path2 = "Łukasz.jpg"

    #path1 = "test_images/imgset0000/QM008.png"
    #path2 = "test_images/imgset0000/QM010.png"

    path1 = "test_images/imgset0594/QM009.png"
    path2 = "test_images/imgset0594/QM016.png"

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    app = ImageComparator(root, path1, path2)
    root.mainloop()
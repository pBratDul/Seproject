from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QSlider, QToolBar, QGraphicsPixmapItem


class ImageComparator(QMainWindow):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        self.setWindowTitle("Image Comparator")

        # Load images
        self.image1 = QImage(image1_path)
        self.image2 = QImage(image2_path)

        # Set initial zoom factor
        self.zoom_factor = 1.0

        # Calculate initial zoom factor to fit the entire image within the window
        window_width = self.screen().size().width()
        window_height = self.screen().size().height()
        initial_zoom_factor = min(window_width / self.image1.width(), window_height / self.image1.height())
        self.zoom_factor = initial_zoom_factor

        # Create graphics scene
        self.scene = QGraphicsScene()
        self.view = CustomGraphicsView(self.scene)  # Use custom QGraphicsView
        self.setCentralWidget(self.view)

        # Create compare slider
        self.compare_slider = QSlider(Qt.Orientation.Horizontal)
        self.compare_slider.setRange(0, 100)
        self.compare_slider.setValue(50)
        self.compare_slider.sliderMoved.connect(self.update_comparison)

        # Create toolbar
        toolbar = self.addToolBar("Image Comparison")
        toolbar.addWidget(self.compare_slider)

        # Display initial images
        self.display_images()

    def display_images(self):
        # Resize images based on zoom factor
        width = int(self.image1.width() * self.zoom_factor)
        height = int(self.image1.height() * self.zoom_factor)

        resized_image1 = self.image1.scaled(width, height)
        resized_image2 = self.image2.scaled(width, height)

        # Get the separation position from the slider
        position = self.compare_slider.value() / 100.0

        # Calculate the separation point
        separation_point = int(position * width)

        # Create two images, one for the left side and one for the right side of the separation point
        left_image = resized_image1.copy(0, 0, separation_point, height)
        right_image = resized_image2.copy(separation_point, 0, width - separation_point, height)

        # Create a composite image by overlaying the second image on top of the first one
        composite_image = QImage(width, height, QImage.Format.Format_RGB32)
        painter = QPainter(composite_image)
        painter.drawImage(0, 0, left_image)
        painter.drawImage(separation_point, 0, right_image)
        painter.end()

        # Display the composite image on the graphics scene
        pixmap = QPixmap.fromImage(composite_image)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)

    def update_comparison(self):
        # Update image comparison based on slider position
        self.display_images()


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setInteractive(True)
        self.setMouseTracking(True)  # Enable mouse tracking to receive mouse move events
        self.last_pan_point = QPointF()

    def wheelEvent(self, event):
        factor = 1.2 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pan_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.pos() - self.last_pan_point
            self.last_pan_point = event.pos()

            # Adjust the delta based on the current zoom factor
            # delta /= self.transform().m11()

            # Update the scroll bars
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())


from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, \
    QSlider, QToolBar, QGraphicsPixmapItem, QPushButton


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

        # Create compare sliders for X and Y axes
        self.compare_slider_x = QSlider(Qt.Orientation.Horizontal)
        self.compare_slider_x.setRange(0, 100)
        self.compare_slider_x.setValue(50)
        self.compare_slider_x.sliderMoved.connect(self.update_comparison)

        self.compare_slider_y = QSlider(Qt.Orientation.Vertical)
        self.compare_slider_y.setRange(0, 100)
        self.compare_slider_y.setValue(50)
        self.compare_slider_y.sliderMoved.connect(self.update_comparison)

        # Create toolbar
        toolbar = self.addToolBar("Image Comparison")
        toolbar.addWidget(self.compare_slider_x)
        toolbar.addWidget(self.compare_slider_y)

        # Create back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        toolbar.addWidget(back_button)

        # Display initial images
        self.display_images()

    def go_back(self):
        # Close the current window
        self.close()

    def display_images(self):
        # Resize images based on zoom factor
        width = int(self.image1.width() * self.zoom_factor)
        height = int(self.image1.height() * self.zoom_factor)

        resized_image1 = self.image1.scaled(width, height)
        resized_image2 = self.image2.scaled(width, height)

        # Get the separation position from the sliders
        position_x = self.compare_slider_x.value() / 100.0
        position_y = 1.0 - (self.compare_slider_y.value() / 100.0)

        # Calculate the separation points
        separation_point_x = int(position_x * width)
        separation_point_y = int(position_y * height)

        # Create four images based on the separation points
        top_left_image = resized_image2.copy(0, 0, separation_point_x, separation_point_y)
        top_right_image = resized_image1.copy(separation_point_x, 0, width - separation_point_x, separation_point_y)
        bottom_left_image = resized_image1.copy(0, separation_point_y, separation_point_x, height - separation_point_y)
        bottom_right_image = resized_image2.copy(separation_point_x, separation_point_y, width - separation_point_x,
                                                 height - separation_point_y)

        # Create a composite image by overlaying the four images
        composite_image = QImage(width, height, QImage.Format.Format_RGB32)
        painter = QPainter(composite_image)
        painter.drawImage(0, 0, top_left_image)
        painter.drawImage(separation_point_x, 0, top_right_image)
        painter.drawImage(0, separation_point_y, bottom_left_image)
        painter.drawImage(separation_point_x, separation_point_y, bottom_right_image)

        # Draw a vertical line at the separation point on the composite image
        painter.setPen(Qt.PenStyle.DashLine)
        painter.drawLine(separation_point_x, 0, separation_point_x, height)

        # Draw a horizontal line at the separation point on the composite image
        painter.drawLine(0, separation_point_y, width, separation_point_y)

        painter.end()

        # Display the composite image on the graphics scene
        pixmap = QPixmap.fromImage(composite_image)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)

    def update_comparison(self):
        # Update image comparison based on slider positions
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

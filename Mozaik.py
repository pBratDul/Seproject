from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QSlider, QToolBar, \
    QGraphicsPixmapItem


class Mozaik(QMainWindow):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        self.setWindowTitle("Mozaik")

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
        toolbar = self.addToolBar("Mozaik")
        toolbar.addWidget(self.compare_slider)

        # Display initial images
        self.display_images()

    def display_images(self):
        # Resize images based on zoom factor
        width = int(self.image1.width() * self.zoom_factor)
        height = int(self.image1.height() * self.zoom_factor)

        resized_image1 = self.image1.scaled(width, height)
        resized_image2 = self.image2.scaled(width, height)

        grid_size = self.compare_slider.value()
        if grid_size == 0: grid_size = 1

        rows = grid_size
        cols = grid_size

        # Calculate the size of each cell in the grid
        cell_width = width // cols
        cell_height = height // rows

        # Create a composite image with a mosaic pattern
        composite_image = QImage(width, height, QImage.Format.Format_RGB32)
        painter = QPainter(composite_image)

        for row in range(rows):
            for col in range(cols):
                # Calculate the starting point of each cell
                cell_x = col * cell_width
                cell_y = row * cell_height

                # Calculate the ending point of each cell
                cell_width_end = cell_width if col < cols - 1 else width - col * cell_width
                cell_height_end = cell_height if row < rows - 1 else height - row * cell_height

                # Use the position to determine which image to use for each cell
                if (row + col) % 2 == 0:
                    source_image = resized_image1
                else:
                    source_image = resized_image2

                # Copy the corresponding region from the source image to the composite image
                cell_image = source_image.copy(cell_x, cell_y, cell_width_end, cell_height_end)

                # Draw the image on the composite image
                painter.drawImage(cell_x, cell_y, cell_image)

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

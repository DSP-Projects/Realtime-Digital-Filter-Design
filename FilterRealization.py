import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class FilterDiagram:
    def __init__(self, b_coeffs, a_coeffs):
        self.b_coeffs = b_coeffs #numerator coefficients
        self.a_coeffs = a_coeffs #denominator coefficients

    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)

        # Set pen and font
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 12))

        # Base positions
        x_start, y_start = 50, 100
        spacing = 80  # Vertical spacing between blocks
        sum_radius = 15  # Radius of summation nodes
        rect_width, rect_height = 40, 40  # Delay block size

        # Draw input line
        painter.drawLine(x_start - 20, y_start, x_start, y_start)
        painter.drawText(x_start - 50, y_start + 5, "x[n]")
        # Draw output line
        painter.drawLine(x_start + 20, y_start, x_start + 220, y_start)
        painter.drawText(x_start + 225, y_start + 5, "y[n]")

        # Draw summation, delay blocks, coefficients, and connections
        for i in range(len(self.a_coeffs)):
            y_pos = y_start + i * spacing

            # Draw summation circle
            painter.drawEllipse(x_start, y_pos - sum_radius, 2 * sum_radius, 2 * sum_radius)
            if i<len(self.a_coeffs)-1:
                painter.drawLine(x_start+10, y_pos+10, x_start+10, y_pos+70)
            painter.drawText(x_start + 5, y_pos + 5, "+")

            # Draw Feedback coefficient(a)
            if i>0:
                painter.drawText(x_start + 40, y_pos - 15, f"a{i}")
                painter.drawLine(x_start + sum_radius * 2, y_pos, x_start + 90, y_pos)#between delay block and summator

            # Draw delay block (except for first node)
        for i in range(1, max(len(self.a_coeffs), len(self.b_coeffs))):
            y_pos = y_start + i * spacing
            painter.drawRect(x_start + 90, y_pos - rect_height // 2, rect_width, rect_height)
            painter.drawText(x_start + 100, y_pos + 5, "Z⁻¹")
            painter.drawLine(x_start + 130, y_pos, x_start + 130, y_start)  #between z-blocks

            # Draw feedfoward coefficients (b) 
        for  i in range (len(self.b_coeffs)):
            y_pos = y_start + i * spacing
            painter.drawText(x_start + 160, y_pos - 15, f"b{i}")
            painter.drawEllipse(x_start+190, y_pos - sum_radius, 2 * sum_radius, 2 * sum_radius)
            painter.drawText(x_start + 195, y_pos + 5, "+")
            if i <len(self.b_coeffs)-1:
                painter.drawLine(x_start+200, y_pos+10, x_start+200, y_pos+70)
            painter.drawLine(x_start+130, y_pos, x_start+190, y_pos)


class DrawingWidget(QWidget):
    def __init__(self, b_coeffs, a_coeffs, parent=None):
        super().__init__(parent)
        self.filter_diagram = FilterDiagram(b_coeffs, a_coeffs)
        self.setMinimumSize(600, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.filter_diagram.draw(painter)

    def save_image(self, filename="filter_diagram.png"):
        pixmap = QPixmap(self.size())  # Create pixmap with widget size
        self.render(pixmap)  # Render the widget to the pixmap
        pixmap.save(filename)  # Save the pixmap as an image

class MainWindow(QMainWindow):
    def __init__(self, b_coeffs, a_coeffs):
        super().__init__()
        self.setWindowTitle("Direct Form II Transposed Filter")
        self.setGeometry(100, 100, 700, 500)

        # Main widget for drawing
        self.drawing_widget = DrawingWidget(b_coeffs, a_coeffs)
        
        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.drawing_widget)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example coefficients
    b = [0.5, -1, 1,5,7]
    a = [0.82, -1.8, 1]

    window = MainWindow(b, a)
    window.show()
    sys.exit(app.exec_())

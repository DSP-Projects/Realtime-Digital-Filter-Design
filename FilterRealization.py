import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QScrollArea
from PyQt5.QtGui import QPainter, QPen, QFont, QPolygonF
import math
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap
from scipy import signal
from PyQt5.uic import loadUi
from CodeGenerator import CodeGenerator

class FilterDiagram:
    def __init__(self, b_coeffs, a_coeffs):
        self.b_coeffs = b_coeffs #numerator coefficients
        self.a_coeffs = a_coeffs #denominator coefficients
        self.sos=signal.tf2sos(self.b_coeffs,self.a_coeffs) #sos: sections of second order for cascade. It returns Nx6 matrix, 
                                     #each row corresponds to [b0, b1, b2, a0, a1, a2]

        print(f"len(self.sos) {(self.sos.shape)}")#to debug

    def draw_direct_form_2(self, painter,b=None, a =None,x_start=300, i=0, key='direct'):

        if key== 'direct':
            a= self.a_coeffs
            b= self.b_coeffs

        painter.setRenderHint(QPainter.Antialiasing)
        # Set pen and font
        pen = QPen(Qt.white, 2)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 9))

        # Base positions
        x_start, y_start = x_start, 50
        spacing = 80  # Vertical spacing between blocks
        sum_radius = 15  # Radius of summation nodes
        rect_width, rect_height = 40, 40  # Delay block size
        
        if i == 0:
            # Draw input line
            painter.drawLine(x_start - 20, y_start, x_start, y_start)
            painter.drawText(x_start - 50, y_start + 5, "x[n]")
            # Draw output line
            painter.drawLine(x_start + 20, y_start, x_start + 220, y_start)
            painter.drawText(x_start + 225, y_start + 5, "y[n]")

        # Draw summation, delay blocks, coefficients, and connections
        for i in range(len(a)):
            y_pos = y_start + i * spacing

            # Draw summation circle
            painter.drawEllipse(x_start, y_pos - sum_radius, 2 * sum_radius, 2 * sum_radius)
            if i<len(a)-1:
                painter.drawLine(x_start+10, y_pos+10, x_start+10, y_pos+70)
            painter.drawText(x_start + 5, y_pos + 5, "+")

            # Draw Feedback coefficient(a)
            if i>0:
                painter.drawText(x_start + 40, y_pos - 15, f"a{i}={a[i]:.2f}")
                painter.drawLine(x_start + sum_radius * 2, y_pos, x_start + 90, y_pos)#between delay block and summator
                self.draw_arrow(painter, x_start + 90, y_pos, x_start + sum_radius * 2, y_pos,)  # Arrow points from (x1,y1) to (x2, y2)

            # Draw delay block (except for first node)
        for i in range(1, max(len(b), len(a))):
            y_pos = y_start + i * spacing
            painter.drawRect(x_start + 90, y_pos - rect_height // 2, rect_width, rect_height)
            painter.drawText(x_start + 100, y_pos + 5, "Z⁻¹")
            painter.drawLine(x_start + 130, y_pos, x_start + 130, y_start)  #between z-blocks

            # Draw feedfoward coefficients (b) 
        for  i in range (len(b)):
            y_pos = y_start + i * spacing
            painter.drawText(x_start + 160, y_pos - 15, f"b{i} = {b[i]:.2f}")
            painter.drawEllipse(x_start+190, y_pos - sum_radius, 2 * sum_radius, 2 * sum_radius)
            painter.drawText(x_start + 195, y_pos + 5, "+")
            if i <len(b)-1:
                painter.drawLine(x_start+200, y_pos+10, x_start+200, y_pos+70)
            painter.drawLine(x_start+130, y_pos, x_start+190, y_pos)
            self.draw_arrow(painter,x_start+130, y_pos, x_start+190, y_pos)

    def draw_cascade(self, painter):
        x_start, y_start=70, 50
        counter=1
        # Draw input line
        painter.drawLine(x_start - 20, y_start, x_start, y_start)
        painter.drawText(x_start - 50, y_start + 5, "x[n]")

        for i, section in enumerate(self.sos):
            b, a = section[:3], section[4:]  # Ignore a0 = 1
            # Ensure each section gets drawn
            self.draw_direct_form_2(painter, b, a, x_start,counter, key='cascade')
            # Move to the next section position
            if i < len(self.sos)-1:
                x_start += 250  
                painter.drawLine(x_start-250, y_start, x_start+200, y_start)
        # Draw output line
        painter.drawLine(x_start+30,y_start, x_start+250, y_start)
        painter.drawText(x_start+250, y_start + 5, "y[n]")
    
    #for drawing arrows:
    def draw_arrow(self, painter, x1, y1, x2, y2, arrow_size=10):
        """ Draws a line with an arrowhead from (x1, y1) to (x2, y2) """
        # Draw the main line
        painter.drawLine(x1, y1, x2, y2)

        # Compute the angle of the line
        angle = math.atan2(y2 - y1, x2 - x1)

        # Calculate arrowhead points
        arrow_p1 = QPointF(x2 - arrow_size * math.cos(angle - math.pi / 6),
                            y2 - arrow_size * math.sin(angle - math.pi / 6))

        arrow_p2 = QPointF(x2 - arrow_size * math.cos(angle + math.pi / 6),
                            y2 - arrow_size * math.sin(angle + math.pi / 6))

        # Draw the arrowhead using a polygon
        arrow_head = QPolygonF([QPointF(x2, y2), arrow_p1, arrow_p2])
        painter.drawPolygon(arrow_head)
    
class DrawingWidget(QWidget):
    def __init__(self, b_coeffs, a_coeffs, name, parent=None):
        super().__init__(parent)
        self.b_coeffs=b_coeffs
        self.a_coeffs=a_coeffs
        self.filter_diagram = FilterDiagram(b_coeffs, a_coeffs)
        self.setMinimumSize(600, 400)
        self.name=name

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.name=='direct':
            self.filter_diagram.draw_direct_form_2(painter, self.b_coeffs, self.a_coeffs)
        elif self.name=='cascade':
            self.filter_diagram.draw_cascade(painter)

    def save_image(self, filename="filter_diagram.png"):
        pixmap = QPixmap(self.size())  # Create pixmap with widget size
        self.render(pixmap)  # Render the widget to the pixmap
        pixmap.save(filename)  # Save the pixmap as an image


class FilterRealizationWindow(QMainWindow):
    def __init__(self, zplane):
        super(FilterRealizationWindow, self).__init__()
        loadUi("FilterRealization.ui", self)
        self.setWindowTitle("Filter Realization")

        self.cascade_widget = self.findChild(QWidget, "cascade")
        self.direct_widget = self.findChild(QWidget, "directForm2")
        b, a = zplane.compute_filter_coefficients()

        # Create scroll areas
        self.cascade_scroll = QScrollArea(self)
        self.direct_scroll = QScrollArea(self)

        # Create drawing widgets
        self.realizing_window_cascade = DrawingWidget(b, a, 'cascade')
        self.realizing_window_direct = DrawingWidget(b, a, 'direct')

        # Configure scrolling behavior
        self.setup_scroll_area(self.cascade_scroll, self.realizing_window_cascade, horizontal=True)
        self.setup_scroll_area(self.direct_scroll, self.realizing_window_direct, vertical=True)

        # Replace original widgets with scrollable areas
        self.cascade_layout = QVBoxLayout(self.cascade_widget)
        self.cascade_layout.addWidget(self.cascade_scroll)

        self.direct_layout = QVBoxLayout(self.direct_widget)
        self.direct_layout.addWidget(self.direct_scroll)

        # Export Button
        self.export_button = self.findChild(QPushButton, "export_2")
        self.export_button.clicked.connect(self.export_filter_realization)

        # Generate C code
        self.code_generator = CodeGenerator(zplane)
        self.generate_code_button = self.findChild(QPushButton, 'generateCode')
        self.generate_code_button.clicked.connect(self.code_generator.generate_c_code)

    def setup_scroll_area(self, scroll_area, widget, horizontal=False, vertical=False):
        """Configures QScrollArea for horizontal or vertical scrolling"""
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)

        if horizontal:
            widget.setMinimumSize(2000, 500)  # Allow large width for cascade form
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        else:
            widget.setMinimumSize(600, 1000)  # Allow large height for direct form
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def export_filter_realization(self):
        self.realizing_window_cascade.save_image("cascade_form.png")
        self.realizing_window_direct.save_image("direct_form.png")
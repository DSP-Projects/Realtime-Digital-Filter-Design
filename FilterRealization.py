import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt
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
        print("(self.sos.shape) ",(self.sos.shape))

    def draw_direct_form_2(self, painter,b=None, a =None,x_start=300, i=0):
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
        if i==0:
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
                painter.drawText(x_start + 40, y_pos - 15, f"a{i}={self.a_coeffs[i]:.2f}")
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
            painter.drawText(x_start + 160, y_pos - 15, f"b{i} = {self.b_coeffs[i]:.2f}")
            painter.drawEllipse(x_start+190, y_pos - sum_radius, 2 * sum_radius, 2 * sum_radius)
            painter.drawText(x_start + 195, y_pos + 5, "+")
            if i <len(self.b_coeffs)-1:
                painter.drawLine(x_start+200, y_pos+10, x_start+200, y_pos+70)
            painter.drawLine(x_start+130, y_pos, x_start+190, y_pos)

    def draw_cascade(self, painter):
        x_start=30
        i=0
        for i in range (len(self.sos)):
            section= self.sos[i]
            b,a= section[:3], section[3:]
            self.draw_direct_form_2(painter, b,a, x_start, i)
            x_start += 150
            i=1
           


        
    
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

        self.cascade_widget= self.findChild(QWidget, "cascade")
        self.direct_widget= self.findChild(QWidget,"directForm2")
        b,a= zplane.compute_filter_coefficients()
        self.realizing_window_cascade= DrawingWidget(b,a, 'cascade', self.cascade_widget)
        self.realizing_window_direct= DrawingWidget(b,a, 'direct', self.direct_widget)
        self.export_button= self.findChild(QPushButton, "export_2")
        self.export_button.clicked.connect(self.export_filter_realization)
        #Generate C code
        self.code_generator= CodeGenerator(zplane)
        self.generate_code_button= self.findChild(QPushButton, 'generateCode')
        self.generate_code_button.clicked.connect(self.code_generator.generate_c_code)

    def export_filter_realization(self):
        self.realizing_window_cascade.save_image("cascade_form.png")
        self.realizing_window_direct.save_image("direct_form.png")

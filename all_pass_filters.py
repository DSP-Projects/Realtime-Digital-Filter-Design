import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class all_pass(QWidget):
    
    def __init__(self, zplane_widget,):
        super().__init__(zplane_widget)
        
        # Matplotlib Figure and Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(zplane_widget)
        layout.addWidget(self.canvas)
        zplane_widget.setLayout(layout)
        # Create subplot
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True)
        # Set tight layout for better fit
        self.figure.tight_layout()

        self.plot_z_plane()


    def plot_z_plane(self, zeros=None, poles=None):
        print (f"zeros in zplane:{zeros} ")
        self.ax.clear()  # Clear any previous plot
        # Plot the unit circle
        theta = np.linspace(0, 2 * np.pi, 100)
        self.ax.plot(np.cos(theta), np.sin(theta), linestyle='--', color='gray', label='Unit Circle')
        # Add labels and grid
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        self.ax.legend()
        self.ax.set_title('Zeros and Poles in the Z-Plane')
        self.ax.set_xlabel('Real Part')
        self.ax.set_ylabel('Imaginary Part')
        self.ax.set_xlim(-2,2)
        zeros = np.array(zeros)if zeros is not None else np.array([])
        poles = np.array(poles)if poles is not None else np.array([])
        print(f"zeros :{zeros}")
        print(f"poles :{poles}")

        if  zeros is not None and zeros.size > 0: # Use .size to check non-empty array
         self.ax.scatter(zeros.real, zeros.imag, s=50, color='red', label='Zeros', marker='o')
        if poles is not None and poles.size > 0:  # Use .size to check non-empty array
         self.ax.scatter(poles.real, poles.imag, s=50, color='blue', label='Poles', marker='x')



        if zeros.size > 0 or poles.size > 0:
            self.ax.legend()

        # Refresh the canvas to reflect the changes
        self.canvas.draw()
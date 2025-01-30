import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
class all_pass:
    
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


    def plot_z_plane(self, zeros, poles):
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

        if zeros.size > 0:
            self.ax.scatter(zeros.real, zeros.imag, s=50, color='red', label='Zeros', marker='o')
        if poles.size > 0:
            self.ax.scatter(poles.real, poles.imag, s=50, color='blue', label='Poles', marker='x')

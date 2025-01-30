import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QCheckBox, QLineEdit, QSlider, QLabel
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QCheckBox, QLineEdit, QSlider, QLabel
from PyQt5.QtCore import Qt


class FilterResponse:
    def __init__(self, mag_plot, phase_plot):
        self.magnitude_plot= mag_plot
        self.phase_plot= phase_plot
        
    @staticmethod
    def compute_filter_response(b, a):
        """Computes frequency response for magnitude (dB) and phase (degrees)."""
        # Compute Frequency Response
        w, h = signal.freqz(b, a)  # w: freq (radians/sample), h: complex response
        
        # Convert to log scale for frequency axis
        frequencies = w  # Normalized frequency (0 to 1)
        
        # Compute Magnitude in dB
        magnitude_db = 20 * np.log10(np.abs(h) + 1e-10)  # Avoid log(0) error
        
        # Compute Phase in Degrees
        phase_deg = np.angle(h, deg=True)  
        
        return frequencies, magnitude_db, phase_deg
    
    def plot_filter_response(self,b, a):
        frequencies, magnitude_db, phase_deg = FilterResponse.compute_filter_response(b, a)
        if self.magnitude_plot:
            self.magnitude_plot.clear()  # Clear the previous plot
            self.magnitude_plot.plot(frequencies, magnitude_db, pen='r')  # Plot with red color

        # Step 4: Update the phase plot with frequencies and phase in degrees
        if self.phase_plot:
            self.phase_plot.clear()  # Clear the previous plot
            self.phase_plot.plot(frequencies, phase_deg, pen='b')
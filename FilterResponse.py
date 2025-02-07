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
    def __init__(self, mag_plot, phase_plot,allpasscorrect):
        self.magnitude_plot= mag_plot
        self.phase_plot= phase_plot
        self.allpasscorrect=allpasscorrect
    @staticmethod
    def compute_filter_response(b, a):
        """Computes frequency response for magnitude (dB) and phase (degrees)."""
        # Compute Frequency Response
        w, h = signal.freqz(b, a)  # w: freq (radians/sample), h: complex response
        
        # Convert to log scale for frequency axis
        frequencies = w  # Normalized frequency (0 to 1)
        
        # Compute Magnitude in dB
        magnitude_db = 20 * np.log10(np.abs(h) + 1e-10)  # Avoid log(0) error
        
        # Compute Phase in radian
        phase_rad = np.unwrap(np.angle(h)) 
        
        return frequencies, magnitude_db, phase_rad
    
    def plot_filter_response(self,b, a):
        frequencies, magnitude_db, phase_rad = FilterResponse.compute_filter_response(b, a)
        phase_deg = np.degrees(phase_rad)

        if self.magnitude_plot:
            self.magnitude_plot.clear()  # Clear the previous plot
            self.magnitude_plot.plot(frequencies, magnitude_db, pen='r')  # Plot with red color
            self.magnitude_plot.setLabel('left', 'Magnitude (dB)')
            self.magnitude_plot.setLabel('bottom', 'Normalized Frequency (rad/sample)')
            self.magnitude_plot.setTitle('Magnitude Response')
        if self.phase_plot:
            self.phase_plot.clear()  # Clear the previous plot
            self.phase_plot.plot(frequencies, phase_deg, pen='b')
            self.phase_plot.setLabel('left', 'Phase (degrees)')
            self.phase_plot.setLabel('bottom', 'Normalized Frequency (rad/sample)')
            self.phase_plot.setTitle('Phase Response')

            self.allpasscorrect.clear()
            self.allpasscorrect.plot(frequencies, phase_deg, pen='b')
            self.allpasscorrect.setLabel('left', 'Phase (degrees)')
            self.allpasscorrect.setLabel('bottom', 'Normalized Frequency (rad/sample)')
            self.allpasscorrect.setTitle('All-Pass Phase Response')

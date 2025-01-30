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
from PyQt5.QtWidgets import QMainWindow,QComboBox, QCheckBox, QRadioButton, QApplication, QPushButton, QLabel, QSlider,QProgressBar, QWidget
from PyQt5.QtGui import QIcon
from pyqtgraph import PlotWidget
import sys
import os
from PyQt5.uic import loadUi
from ZPlane import ZPlane
from FilterRealization import FilterRealizationWindow
from FilterResponse import FilterResponse 
from scipy import signal
import numpy as np



class AllPassFilter:
    def __init__(self, a=0.5):
        self.a = a

    def get_coefficients(self):
        """Get the coefficients for the all-pass filter."""
        b = np.array([1, -self.a])
        a = np.array([1, -self.a])
        zeros, poles, _ = signal.tf2zpk(b, a)
        return zeros, poles

   

       

    def plot_phase_response(self):
        """Plot the phase response of the all-pass filter."""
        b, a = self.get_coefficients()
        w, h = signal.freqz(b, a, worN=8000)
        phase_deg = np.angle(h, deg=True)

        
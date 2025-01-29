from PyQt5.QtWidgets import QMainWindow,QComboBox, QCheckBox, QRadioButton, QApplication, QPushButton, QLabel, QSlider,QProgressBar
from PyQt5.QtGui import QIcon
from pyqtgraph import PlotWidget
import sys
import os
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)
        self.setWindowTitle("Real-time Digital Filter Design")

        #filter design (fatma)

        #zero-pole radiobuttons
        self.zero_radioButton = self.findChild(QRadioButton, "zeros")
        self.pole_radioButton = self.findChild(QRadioButton, "poles")
        self.zero_radioButton.setChecked(True)
        self.zero_radioButton.clicked.connect(self.zero_pole_placement)
        self.pole_radioButton.clicked.connect(self.zero_pole_placement)
        #conjugate check box
        self.conjugate_check = self.findChild(QCheckBox, "conjugateCheck")
        self.conjugate_check.clicked.connect(self.check_conjugate)
        #clearing
        self.clear_combobox = self.findChild(QComboBox,"clearCombo")
        self.clear_combobox.currentIndexChanged.connect(self.clear_combobox_index)

        self.clear_button = self.findChild(QPushButton,"clear")
        self.clear_button.clicked.connect(self.clear)

        #swapping
        self.swap = self.findChild(QComboBox,"swapping")

        #undo & redo
        self.undo_button = self.findChild(QPushButton,"undo")
        self.redo_button = self.findChild(QPushButton,"redo")

        #z-plane
        self.z_plane = self.findChild(PlotWidget, "z_plane")

        #magnitude plot
        self.magnitude_plot = self.findChild(PlotWidget, "Magnitude_graph")
        
        #phase plot
        self.phase_plot = self.findChild(PlotWidget, "Phase_graph")

    def zero_pole_placement(self):
        pass
    
    def check_conjugate(self):
        pass
    
    def clear_combobox_index(self):
      index = self.clear_combobox.currentIndex()

    def clear(self,index):
        pass  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())         
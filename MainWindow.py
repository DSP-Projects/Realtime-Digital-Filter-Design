from PyQt5.QtWidgets import QMainWindow,QComboBox, QCheckBox, QRadioButton, QApplication, QPushButton, QLabel, QSlider,QProgressBar
from PyQt5.QtGui import QIcon
from pyqtgraph import PlotWidget
import sys
import os
from PyQt5.uic import loadUi
from ZPlane import ZPlane
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)
        self.setWindowTitle("Real-time Digital Filter Design")

        #z-plane
        self.z_plane_widget = self.findChild(PlotWidget, "z_plane")
        self.zplane= ZPlane(self.z_plane_widget)
        #filter design (fatma)

        #zero-pole radiobuttons
        self.zero_radioButton = self.findChild(QRadioButton, "zeros")
        self.pole_radioButton = self.findChild(QRadioButton, "poles")
        self.zero_radioButton.setChecked(True)
        self.zero_radioButton.clicked.connect(self.zplane.toggle_mode_to_zeros)
        self.pole_radioButton.clicked.connect(self.zplane.toggle_mode_to_poles)
        #conjugate check box
        self.conjugate_check = self.findChild(QCheckBox, "conjugateCheck")
        self.conjugate_check.clicked.connect(self.zplane.toggle_conjugate)
        #clearing
        self.clear_combobox = self.findChild(QComboBox,"clearCombo")
        self.clear_button = self.findChild(QPushButton,"clear")
        self.clear_button.clicked.connect(self.clear_plane)
        self.delete= self.findChild(QCheckBox, "delete_2")
        self.delete.clicked.connect(self.zplane.toggle_delete)

        #swapping
        self.swap = self.findChild(QComboBox,"swapping")
        self.swap.currentIndexChanged.connect(lambda index: self.zplane.swap_zeros_poles(index))

        #undo & redo
        self.undo_button = self.findChild(QPushButton,"undo")
        self.redo_button = self.findChild(QPushButton,"redo")
        self.undo_button.clicked.connect(self.zplane.undo)
        self.redo_button.clicked.connect(self.zplane.redo)

        #save and load
        self.save= self.findChild(QPushButton, "save")
        self.load= self.findChild(QPushButton, "load")
        self.save.clicked.connect(self.zplane.save_filter)
        self.load.clicked.connect(self.zplane.load_from_file)

        #magnitude plot
        self.magnitude_plot = self.findChild(PlotWidget, "Magnitude_graph")
        #phase plot
        self.phase_plot = self.findChild(PlotWidget, "Phase_graph")

    def clear_plane(self):
        index = self.clear_combobox.currentIndex()
        match index:
            case 0:
                self.zplane.clear_zeros()
            case 1: 
                self.zplane.clear_poles()
            case 2:
                self.zplane.clear_all()
          

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())         
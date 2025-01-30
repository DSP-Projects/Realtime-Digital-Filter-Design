from PyQt5.QtWidgets import QMainWindow,QComboBox, QCheckBox, QRadioButton, QApplication, QPushButton, QLabel, QSlider,QProgressBar, QWidget
from PyQt5.QtWidgets import QMainWindow,QComboBox, QCheckBox, QRadioButton, QApplication, QPushButton, QLabel, QSlider,QProgressBar,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QIcon
from pyqtgraph import PlotWidget
import sys
import os
from PyQt5.uic import loadUi
from ZPlane import ZPlane
from RealTimeSignal import RealTimeFilter, RealTimePlot
from Load import Load
import pandas as pd
from FilterRealization import FilterRealizationWindow 
from FilterResponse import FilterResponse 
from scipy import signal
from RealTimeSignal import RealTimeFilter, RealTimePlot
from Load import Load
import pandas as pd
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)
        self.setWindowTitle("Real-time Digital Filter Design")


        self.filter_library = {
            "Butterworth LPF": {"order": 4, "type": "butter", "btype": "low"},
            "Butterworth HPF": {"order": 4, "type": "butter", "btype": "high"},
            "Butterworth BPF": {"order": 4, "type": "butter", "btype": "band"},
            "Chebyshev-1 LPF": {"order": 4, "type": "cheby1", "rp": 1, "btype": "low"},
            "Chebyshev-1 HPF": {"order": 4, "type": "cheby1", "rp": 1, "btype": "high"},
            "Chebyshev-1 BPF": {"order": 4, "type": "cheby1", "rp": 1, "btype": "band"},
            "Chebyshev-2 LPF": {"order": 4, "type": "cheby2", "rs": 40, "btype": "low"},
            "Chebyshev-2 HPF": {"order": 4, "type": "cheby2", "rs": 40, "btype": "high"},
            "Chebyshev-2 BPF": {"order": 4, "type": "cheby2", "rs": 40, "btype": "band"},
            "Elliptic LPF": {"order": 4, "type": "ellip", "rp": 1, "rs": 40, "btype": "low"},
            "Elliptic HPF": {"order": 4, "type": "ellip", "rp": 1, "rs": 40, "btype": "high"},
            "Elliptic BPF": {"order": 4, "type": "ellip", "rp": 1, "rs": 40, "btype": "band"},
            "Bessel LPF": {"order": 4, "type": "bessel", "btype": "low"},
            "Bessel HPF": {"order": 4, "type": "bessel", "btype": "high"}
        }

        self.combo_library=self.findChild(QComboBox,"libraries")
        self.setup_combo_box()
        self.combo_library.currentIndexChanged.connect(self.load_filter_with_allpass)

        #magnitude plot
        self.magnitude_plot = self.findChild(PlotWidget, "Magnitude_graph")
        #phase plot
        self.phase_plot = self.findChild(PlotWidget, "Phase_graph")
        #filter_response instance
        self.filter_response= FilterResponse(self.magnitude_plot, self.phase_plot)
        self.real_time_filter=RealTimeFilter()

        #z-plane
        self.z_plane_widget = self.findChild(QWidget, "widget_3")
        self.zplane= ZPlane(self.z_plane_widget, self.filter_response, self.real_time_filter)

        #judy
        self.original_plot=self.findChild(PlotWidget,"real_signal")
        self.filtered_plot=self.findChild(PlotWidget,"filteredSignal")
        self.graphics_view=self.findChild(QGraphicsView,"touch_pad")
        self.graphics_view.setScene(QGraphicsScene())

        self.load_radiobutton= self.findChild(QRadioButton,"loadSignal")
        self.touch_button= self.findChild(QRadioButton,"touchPad")

        self.load_pushbutton=self.findChild(QPushButton,"loadButton")
        self.speed_slider=self.findChild(QSlider,"speedSlider")

        self.load_pushbutton.clicked.connect(self.set_signal)
        self.signal_data_time = []
        self.signal_data_amplitude = []
        self.load_signal= Load()
        self.real_time_plot=RealTimePlot(self.real_time_filter,self.original_plot,self.filtered_plot,self.graphics_view,self.signal_data_time,self.signal_data_amplitude)

        self.speed_slider.valueChanged.connect(self.real_time_plot.update_timer)
        self.touch_button.clicked.connect(self.set_touch_mode)
        self.load_radiobutton.clicked.connect(self.set_load_mode)


        #realization
        self.filter_realization = self.findChild(QPushButton,"filterRealization")
        self.filter_realization.clicked.connect(self.open_filter_realization_window)
        
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
        self.clear_button.clicked.connect(self.clear_plane)

        #swapping
        self.swap = self.findChild(QPushButton,"swapButton")
        self.swap.clicked.connect(self.zplane.swap_zeros_poles)

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



        

    #judy
    def set_signal(self):
        print(2)
        self.file_path = self.load_signal.browse_signals()
        if self.file_path:
            csvFile = pd.read_csv(self.file_path)
            self.signal_data_time = csvFile.iloc[:, 0].values
            self.signal_data_amplitude = csvFile.iloc[:, 1].values
            self.real_time_plot.signal_time = self.signal_data_time
            self.real_time_plot.signal_amplitude = self.signal_data_amplitude
            self.real_time_plot.counter = 0  # Reset the counter


    def set_touch_mode(self):
        self.real_time_plot.mode = "touch"
        self.real_time_plotsignal = []  # Clear signal for touch mode
        self.real_time_filter.counter = 0  # Reset counter

        self.real_time_plot.original_data.clear()  # Clear data for original signal
        self.real_time_plot.filtered_data.clear()  # Clear data for filtered signal
        self.real_time_plot.original_curve.setData([])  # Clear plot
        self.real_time_plot.filtered_curve.setData([])  # Clear plot
        

    def set_load_mode(self):
        self.real_time_plot.mode = "load"
        self.real_time_plot.signal = []  # Clear signal for load mode
        self.real_time_plot.counter = 0  # Reset counter
        self.real_time_plot.original_data.clear()  # Clear data for original signal
        self.real_time_plot.filtered_data.clear()  # Clear data for filtered signal
        self.real_time_plot.original_curve.setData([])  # Clear plot
        self.real_time_plot.filtered_curve.setData([])  # Clear plot   
    
    #fatma
    def clear_plane(self):
        index = self.clear_combobox.currentIndex()
        match index:
            case 0:
                self.zplane.clear_zeros()
            case 1: 
                self.zplane.clear_poles()
            case 2:
                self.zplane.clear_all()
    
    def open_filter_realization_window(self):
        self.filter_realization_window = FilterRealizationWindow(self.zplane)
        self.filter_realization_window.show()
    
    #hajer
    def setup_combo_box(self):
     """Initialize the combo box with a placeholder and filter names."""
     self.combo_library.addItem("Select Built-in Library Filters")  # Add placeholder
     self.combo_library.addItems(self.filter_library.keys())  # Add actual filters
     self.combo_library.setCurrentIndex(0)

    def setup_combo_box(self):
     """Initialize the combo box with a placeholder and filter names."""
     self.combo_library.addItem("Select Built-in Library Filters")  # Add placeholder
     self.combo_library.addItems(self.filter_library.keys())  # Add actual filters
     self.combo_library.setCurrentIndex(0)

    def load_filter_with_allpass(self):
        """Load and apply the filter with all-pass elements."""
        # Get the selected filter from the combo box
        selected_filter = self.combo_library.currentText()
        if selected_filter == "Select Built-in Library Filters":
         print("Please select a valid filter from the library.")
         return
        
        if not selected_filter:
            print("Invalid filter selection")
            return     

        filter_params = self.filter_library.get(selected_filter, None)
        if filter_params is None:
            print("No filter parameters found for the selected filter.")
            return

        # Extract filter parameters
        filter_type = filter_params["type"]
        order = filter_params["order"]
        btype = filter_params["btype"]
        if btype == "band":
         btype = "bandpass"  # Correct naming for SciPy
        elif btype == "stop":
         btype = "bandstop"

        # Create the filter using scipy
        if btype in ["bandpass", "bandstop"]:
         wp = [0.2, 0.5]  # Example: Bandpass from 0.2 to 0.5 (normalized)
         ws = [0.15, 0.55] 
        else:
         wp = 0.25  
         ws = 0.35 
        if filter_type == "butter":
            b, a = signal.butter(order, wp, btype=btype, output='ba')
        elif filter_type == "cheby1":
            rp = filter_params["rp"]
            b, a = signal.cheby1(order, rp, wp, btype=btype, output='ba')
        elif filter_type == "cheby2":
            rs = filter_params["rs"]
            b, a = signal.cheby2(order, rs, ws, btype=btype, output='ba')
        elif filter_type == "ellip":
            rp = filter_params["rp"]
            rs = filter_params["rs"]
            b, a = signal.ellip(order, rp, rs, wp, btype=btype, output='ba')
        elif filter_type == "bessel":
            b, a = signal.bessel(order, wp, btype=btype, output='ba')
        self.filter_response.plot_filter_response(b, a)
        self.zplane.compute_zeros_poles_from_coefficients(b,a)

        return b,a
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())         
import sys
import time
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPushButton, QFileDialog, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent
from pyqtgraph import PlotWidget, mkPen
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt

class RealTimeFilter:
    def __init__(self):
        self.b = None
        self.a = None
        self.input_buffer = np.zeros(1)
        self.output_buffer = np.zeros(1)

    def set_coef(self, b, a):
        # Normalize coefficients if necessary
        if a[0] != 1:
            a = a / a[0]
            b = b / a[0]
        
        self.b = b
        self.a = a
        self.input_buffer = np.zeros(len(self.b))
        self.output_buffer = np.zeros(len(self.a))

    def apply_filter(self, x):
        # Shift buffers
        self.input_buffer[1:] = self.input_buffer[:-1]
        self.output_buffer[1:] = self.output_buffer[:-1]

        # Add new input
        self.input_buffer[0] = x

        # Calculate output using the difference equation
        y = np.dot(self.b, self.input_buffer) - np.dot(self.a[1:], self.output_buffer[1:])
        self.output_buffer[0] = y
        return y




class RealTimePlot(QWidget):
 
    def __init__(self, filter_instance, original_curve_widget,filtered_curve_widget,graphics_view,signal_time,signal_amplitude):
        super().__init__()
        
        self.filter_instance = filter_instance
        self.original_plot_widget=original_curve_widget
        self.filtered_plot_widget=filtered_curve_widget
        
        self.original_curve = self.original_plot_widget.plot(pen=mkPen(color="#ab7b96", width=2))
        self.original_data = []

        self.filtered_curve = self.filtered_plot_widget.plot(pen=mkPen(color="#592842", width=2))
        self.filtered_data = []
        self.signal_time=signal_time
        self.signal_amplitude=signal_amplitude
        self.scene = graphics_view.scene()
        self.last_pos = None
        self.mode="load"
        self.signal = []

        self.graphics_view = graphics_view
        self.graphics_view.viewport().installEventFilter(self)
        # Timer for real-time update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  

        self.signal = []  # Original signal (e.g., test signal)
        self.filtered_signal = []  # Filtered signal
        self.counter = 0

        self.last_time = time.time()  # Store the last time the mouse moved
        self.phase = 0 

        self.is_generating_signal = False  # Flag for signal generation
        self.last_mouse_pos = None  # Store the last mouse position for velocity calculation

        self.graphics_view.setMouseTracking(True)
        self.graphics_view.viewport().installEventFilter(self)

    def update_timer(self, value):
        self.timer.setInterval(1000 // value)

    def update_plot(self):
        if self.mode == "load":
            if self.counter < len(self.signal_time):
                # Use the signal data directly in load mode
                x = self.signal_amplitude[self.counter]  # Amplitude value
                y = self.filter_instance.apply_filter(x)

                self.original_data.append(x)
                self.filtered_data.append(y)

                if len(self.original_data) > 500:
                    self.original_data.pop(0)
                    self.filtered_data.pop(0)

                self.original_curve.setData(self.signal_time[:self.counter + 1], self.original_data)
                self.filtered_curve.setData(self.signal_time[:self.counter + 1], self.filtered_data)
                self.counter += 1
        elif self.mode == "touch":
            # Keep the existing logic for touch mode
         
            if self.counter < len(self.signal):
                x = self.signal[self.counter]
                y = self.filter_instance.apply_filter(x)

                self.original_data.append(x)
                self.filtered_data.append(y)

                if len(self.original_data) > 5000:
                    self.original_data.pop(0)
                    self.filtered_data.pop(0)

                self.original_curve.setData(self.original_data)
                self.filtered_curve.setData(self.filtered_data)
                self.counter += 1



    def add_signal(self, new_signal):
        self.signal = new_signal
        self.counter = 0


    def eventFilter(self, source, event):
        if source is not None and source  == self.graphics_view.viewport() and event.type() == event.MouseMove:
            self.mouse_move_event(event)
        return super().eventFilter(source, event)

    def mouse_move_event(self, event):
        if self.mode != "touch":
            return  

        pos = self.graphics_view.mapToScene(event.pos())
        current_time = time.perf_counter()  # Higher precision
        delta_time = current_time - self.last_time
        self.last_time = current_time  

        if self.last_pos is not None and delta_time > 0:
            velocity = np.sqrt((pos.x() - self.last_pos.x())**2 + (pos.y() - self.last_pos.y())**2) / delta_time

            
            min_freq = 0.5   
            max_freq = 100   

            
            mapped_frequency = np.clip(5 * np.log1p(velocity), min_freq, max_freq)  

          
            self.phase += 2 * np.pi * mapped_frequency * delta_time  # Update phase
            signal_value = np.sin(self.phase)  # Generate sine wave

            self.signal.append(signal_value/20)

            if len(self.signal) > 5000:
                self.signal.pop(0)

        self.last_pos = pos





    def update_signal_label(self):
        if self.signal:
            display_signal = ", ".join(f"{x:.2f}" for x in self.signal[-10:])  # Show last 10 points
            print(f"Generated Signal: [{display_signal}]")
        else:
            print("Generated Signal: [No data yet]")

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy import signal
import csv

class ZPlane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Zeros and Poles
        self.zeros = np.array([], dtype=complex)
        self.poles = np.array([], dtype=complex)
        self.pole_mode= False 
        self.dragging = None #for dragging event
        self.delete_mode=  False
        self.conjugate_mode= False

        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []
        
        # Matplotlib Figure and Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.ax = self.figure.add_subplot(111)
        
        self.plot_z_plane()
        #mouse connection
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_release)
    
    #Undo/Redo Functionality
    def save_state(self): #before change, save the current state first
        self.undo_stack.append((self.zeros.copy(), self.poles.copy()))
        self.redo_stack.clear()  # Clear redo stack when a new change is made

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append((self.zeros.copy(), self.poles.copy()))  # Save current state to redo
            self.zeros, self.poles = self.undo_stack.pop()  # Restore previous state
            self.plot_z_plane()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append((self.zeros.copy(), self.poles.copy()))  # Save current state to undo
            self.zeros, self.poles = self.redo_stack.pop()  # Restore redone state
            self.plot_z_plane()

    def plot_z_plane(self):
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
        self.ax.axis('equal')

        if self.zeros.size > 0:
            self.ax.scatter(self.zeros.real, self.zeros.imag, s=50, color='red', label='Zeros', marker='o')
        if self.poles.size > 0:
            self.ax.scatter(self.poles.real, self.poles.imag, s=50, color='blue', label='Poles', marker='x')
        
        # Refresh the canvas
        self.canvas.draw()
        

    def toggle_mode(self, mode_button):
        self.pole_mode= not self.pole_mode
        mode = "Pole Mode" if self.pole_mode else "Zero Mode"
        mode_button.setText(f"Toggle Mode (Current: {mode})")
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        
        click_pos = complex(event.xdata, event.ydata)
        tolerance = 0.05  # Distance threshold for selecting a point
        self.dragging = None

        # Check if the click is near an existing zero or pole
        if self.pole_mode and len(self.poles)!=0:
            distances = np.abs(self.poles - click_pos)
            if distances.min() < tolerance:
                self.dragging = ('pole', distances.argmin()) #returns the index of the minimum value
        elif len(self.zeros)!=0:
            distances = np.abs(self.zeros - click_pos)
            if distances.min() < tolerance:
                self.dragging = ('zero', distances.argmin())
        
        if self.delete_mode:
            self.save_state()
            point_type, index = self.dragging
            if point_type =='pole':
               self.poles= np.delete(self.poles, index)
            elif point_type =='zero':
                self.zeros= np.delete(self.zeros, index)
            self.plot_z_plane()

        # If neither dragging an existing point nor deleting, add a new one at this position
        elif self.dragging is None:
            self.save_state()
            if self.pole_mode:
                new_pole = click_pos #get data coordinates relative to the plot
                self.poles = np.append(self.poles, new_pole)
                self.ax.scatter(new_pole.real,new_pole.imag, s=50, color='blue', label='Poles', marker='x')
                if self.conjugate_mode and click_pos.imag != 0:
                    self.poles = np.append(self.poles, new_pole.conjugate())
                    self.ax.scatter(new_pole.real,-1*new_pole.imag, s=50, color='blue', label='Poles', marker='x')
            
            elif not self.pole_mode: 
                new_zero= click_pos
                self.zeros = np.append(self.zeros, new_zero)
                self.ax.scatter(new_zero.real, new_zero.imag, s=50, color='red', label='Zeros', marker='o')
                if self.conjugate_mode and click_pos.imag != 0:
                    self.zeros = np.append(self.zeros, new_zero.conjugate())
                    self.ax.scatter(new_zero.real, -1*new_zero.imag, s=50, color='red', label='Zeros', marker='o')
            self.canvas.draw()
    
    def on_mouse_move(self, event):
        if self.dragging and event.inaxes == self.ax:
        # Update the position of the dragged point
            new_pos = complex(event.xdata, event.ydata)
            point_type, index = self.dragging
            if point_type == 'pole':
                self.poles[index] = new_pos
            elif point_type == 'zero':
                self.zeros[index] = new_pos

    def on_release(self, event):
        if self.dragging:
            self.save_state()
            self.plot_z_plane()
            self.dragging = None

    def clear_all(self):
        self.save_state()
        self.poles= np.array([], dtype=complex)
        self.zeros= np.array([], dtype=complex)
        self.plot_z_plane()
    
    def clear_poles(self):
        self.save_state()
        self.poles= np.array([], dtype=complex)
        self.plot_z_plane()

    def clear_zeros(self):
        self.save_state()
        self.zeros= np.array([], dtype=complex)
        self.plot_z_plane()

    def toggle_delete(self):
        self.delete_mode= not self.delete_mode
        return self.delete_mode
    
    def toggle_conjugate(self):
        self.conjugate_mode= not self.conjugate_mode
    
    def swap_zeros_poles(self):
        self.save_state()
        self.poles, self.zeros = self.zeros, self.poles
        self.plot_z_plane()

    def compute_filter_coefficients(self):
        b = np.poly(self.zeros)
        a = np.poly(self.poles)
        return a,b
    
    def get_poles(self):
        return self.poles
    
    def get_zeros(self):
        return self.zeros


    def save_filter(self): #save poles and zeros into csv file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)", options=options)

        if not file_path:
            return  # User canceled the save operation

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Real", "Imaginary"])
            # Save zeros
            for z in self.zeros:
                writer.writerow(["zero", z.real, z.imag])
            # Save poles
            for p in self.poles:
                writer.writerow(["pole", p.real, p.imag])

    def load_from_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load File", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options)

        if not file_path:
            return  # User canceled the load operation
        
        zeros, poles = [], []
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == "zero":
                    zeros.append(complex(float(row[1]), float(row[2])))
                elif row[0] == "pole":
                    poles.append(complex(float(row[1]), float(row[2])))

        # Save state before loading new data
        self.save_state()
        #convert lists to numpy arrays 
        self.zeros = np.array(zeros, dtype=complex)
        self.poles = np.array(poles, dtype=complex)
        self.plot_z_plane()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create a main window
    main_window = QMainWindow()
    main_window.setWindowTitle("Z-Plane Tester")

    # Initialize ZPlane widget
    z_plane_widget = ZPlane()
    z_plane_widget.zeros = np.array([], dtype=complex)  # Initialize zeros array
    z_plane_widget.poles = np.array([], dtype=complex)  # Initialize poles array

    # Add ZPlane widget to main window
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)

    # Add toggle button for mode
    from PyQt5.QtWidgets import QPushButton

    def toggle_mode():
        z_plane_widget.pole_mode = not z_plane_widget.pole_mode
        mode = "Pole Mode" if z_plane_widget.pole_mode else "Zero Mode"
        mode_button.setText(f"Toggle Mode (Current: {mode})")

    def toggle_delete():
        mode= z_plane_widget.toggle_delete()
        delete_button.setText(f"Toggle Delete (Current: {mode})")

    mode_button = QPushButton("Toggle Mode (Current: Zero Mode)")
    mode_button.clicked.connect(toggle_mode)
    clear_button = QPushButton("Clear all")
    clear_button.clicked.connect(z_plane_widget.clear_all)
    delete_button = QPushButton("Delete")
    delete_button.clicked.connect(toggle_delete)
    swap_button = QPushButton("Swap")
    swap_button.clicked.connect(z_plane_widget.swap_zeros_poles)


    main_layout.addWidget(mode_button)
    main_layout.addWidget(clear_button)
    main_layout.addWidget(delete_button)
    main_layout.addWidget(z_plane_widget)
    main_layout.addWidget(swap_button)

    main_window.setCentralWidget(main_widget)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec_())
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy import signal
import csv

class ZPlane(QWidget):
    def __init__(self, zplane_widget):
        super().__init__(zplane_widget)
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
        layout = QVBoxLayout(zplane_widget)
        layout.addWidget(self.canvas)
        zplane_widget.setLayout(layout)
        # Create subplot
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True)
        # Set tight layout for better fit
        self.figure.tight_layout()
        
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

        if self.zeros.size > 0:
            self.ax.scatter(self.zeros.real, self.zeros.imag, s=50, color='red', label='Zeros', marker='o')
        if self.poles.size > 0:
            self.ax.scatter(self.poles.real, self.poles.imag, s=50, color='blue', label='Poles', marker='x')
        
        # Refresh the canvas
        self.canvas.draw()
        

    def toggle_mode_to_zeros(self):
        self.pole_mode= False
    def toggle_mode_to_poles(self):
        self.pole_mode= True
   
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
    
    def toggle_conjugate(self):
        self.conjugate_mode= not self.conjugate_mode
    
    def swap_zeros_poles(self, index):
        self.save_state()
        if index==0:
            self.poles= self.zeros
        elif index==1:
            self.zeros= self.poles
        self.plot_z_plane()
    
    def enforce_conjugate_pairs(self,arr):
        arr_conj = np.conj(arr[np.iscomplex(arr)])
        return np.hstack([arr, arr_conj])
    
    def compute_filter_coefficients(self):
        z = self.enforce_conjugate_pairs(self.zeros)
        p = self.enforce_conjugate_pairs(self.poles)
        b,a = signal.zpk2tf(z, p, 1)
        return b,a
    
    def compute_zeros_poles_from_coefficients(self, b,a):
       self.zeros, self.poles,_ =signal.tf2zpk(b,a)
       self.plot_z_plane()
    
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



from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot

class Load:
    def __init__(self):
        self.file_path = None
        self.file_extension = None
        self.file_path_list = []  # Initialize the list here

    @pyqtSlot()
    def browse_signals(self):
        self.file_path, _ = QFileDialog.getOpenFileName(None, "Open Signal File", "", "Signal Files (*.csv )")
        if self.file_path:
            self.file_extension = self.file_path.split('.')[-1].lower()
            if self.check_extension():
                return self.file_path
        else:
            QMessageBox.warning(None, "No file selected", "Please select a signal file to upload.")

    def check_extension(self):
        if self.file_extension not in ['csv', 'edf', 'hdf5']:
            QMessageBox.warning(None, "Unsupported File", "The selected file type is not supported.")
        else:
            self.file_path_list.append(self.file_path)
            return True
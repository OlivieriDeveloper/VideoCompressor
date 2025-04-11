# main.py
#
# Copyright (C) 2025 [Il Tuo Nome]
#
# This file is part of VideoCompressor.
#
# VideoCompressor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# VideoCompressor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton
import os
import subprocess
from compressor import Video

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Set Application Data
        self.filename = ""
        self.filepath = ""
        self.filext = ""
        self.bfilesize = 0
        self.mbfilesize = 100
        self.nsize = 0
        self.nfilename = ""
        self.v1 = None
        self.compressed_dir = ""

        MainWindow.setObjectName("Video Compressor")
        MainWindow.resize(500, 200)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # File Selection
        self.sel_file_label = QtWidgets.QLabel(self.centralwidget)
        self.sel_file_label.setGeometry(QtCore.QRect(30, 20, 501, 16))
        self.sel_file_label.setObjectName("sel_file_label")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 40, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFileDialog)

        # Size Selection
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 70, 221, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setTickInterval(10)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.valueChanged.connect(self.slider_change)
        
        self.nsize_label = QtWidgets.QLabel(self.centralwidget)
        self.nsize_label.setGeometry(QtCore.QRect(260, 70, 81, 16))
        self.nsize_label.setObjectName("nsize_label")

        # Compression Controls
        self.compress_btn = QtWidgets.QPushButton(self.centralwidget)
        self.compress_btn.setGeometry(QtCore.QRect(30, 100, 75, 23))
        self.compress_btn.setObjectName("compress_btn")
        self.compress_btn.clicked.connect(self.compress_callback)

        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(30, 120, 120, 23))
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.stop_compressing)
        self.stop_btn.hide()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Compressor"))
        self.sel_file_label.setText(_translate("MainWindow", "Selected File: "))
        self.pushButton.setText(_translate("MainWindow", "Select File"))
        self.nsize_label.setText(_translate("MainWindow", "New Dimension"))
        self.compress_btn.setText(_translate("MainWindow", "Compress"))
        self.stop_btn.setText(_translate("MainWindow", "Stop Compression"))
    
    def getFilePathNameExt(self, filepath):
        tmp = filepath.split("/")
        tmp = tmp[-1]
        filename, filext = tmp.split(".")
        return (filepath, filename, filext)

    def setFileSize(self):
        if self.filename:
            self.bfilesize = os.path.getsize(self.filepath)
            self.mbfilesize = self.bfilesize / (2**20)
        
    def openFileDialog(self):
        # Ottieni il percorso della cartella Video di Windows
        videos_path = os.path.expanduser("~/Videos")
        fname = QFileDialog.getOpenFileName(None, "Open File", videos_path, "MP4 Files (*.mp4);;MOV Files (*.mov);;MKV Files (*.mkv)")
        if fname[0]:
            self.sel_file_label.setText(f"Selected File: {fname[0]}")
            self.filepath, self.filename, self.filext = self.getFilePathNameExt(fname[0])
            self.setFileSize()
            self.horizontalSlider.setMinimum(0)
            self.horizontalSlider.setMaximum(int(self.mbfilesize))

    def slider_change(self):
        self.nsize = self.horizontalSlider.value()
        self.nsize_label.setText(f"New size: {self.nsize} MB")
    
    def open_compressed_folder(self):
        if self.compressed_dir:
            # Converti il percorso in un percorso assoluto e normalizzato
            abs_path = os.path.abspath(self.compressed_dir)
            # Sostituisci le barre rovesciate con barre normali per Windows
            windows_path = abs_path.replace('/', '\\')
            # Apri l'explorer con il percorso corretto
            subprocess.Popen(f'explorer "{windows_path}"')
    
    def compress_callback(self):
        if not self.filename:
            QMessageBox.warning(None, "Warning", "Please select a file first")
            return

        print(f"File Infos: \n - Filename: {self.filename}\n - File Type: {self.filext}\n - File Path: {self.filepath}\n - New Size: {self.nsize}\n")
        
        # Crea la directory compressed se non esiste
        self.compressed_dir = os.path.join(os.path.dirname(self.filepath), "compressed")
        if not os.path.exists(self.compressed_dir):
            os.makedirs(self.compressed_dir)

        self.v1 = Video(filename=self.filename, 
                        filepath=self.filepath,
                        filext=self.filext)
        
        print("Compressing...")
        self.compress_btn.hide()
        self.stop_btn.show()
        
        output_path = os.path.join(self.compressed_dir, f"{self.filename}_compressed.{self.filext}")
        self.v1.compress_video(nDim=self.nsize, output=output_path)
        
        # Timer per controllare lo stato della compressione
        self.compression_timer = QtCore.QTimer()
        self.compression_timer.timeout.connect(self.check_compression_status)
        self.compression_timer.start(100)  # Controlla ogni 100ms
    
    def check_compression_status(self):
        if self.v1.compression_complete:
            print("Compression complete...")
            self.compress_btn.show()
            self.stop_btn.hide()
            self.compression_timer.stop()
            
            # Crea il messaggio con il pulsante per aprire la cartella
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Compression completed successfully!")
            msg.setIcon(QMessageBox.Information)
            
            # Aggiungi il pulsante per aprire la cartella
            open_folder_btn = QPushButton("Open Compressed Folder")
            open_folder_btn.clicked.connect(self.open_compressed_folder)
            msg.addButton(open_folder_btn, QMessageBox.ActionRole)
            
            # Aggiungi il pulsante OK
            msg.addButton(QMessageBox.Ok)
            
            msg.exec_()
        
    def stop_compressing(self):
        if self.v1:
            self.v1.stop_compression()
            print("Stop compression...")
            self.compress_btn.show()
            self.stop_btn.hide()
            self.compression_timer.stop()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

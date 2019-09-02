#!/usr/bin/env python3

import sys
import time 
import threading
import pyaudio
import wave
import atexit
from random import randrange
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.QtCore import QTimer
from guiTest1 import *

class AudioPlayer(object):

    def __init__(self):
        self.CHUNK = 8192 #1024 
        self.START_POINT = 0
        self.frames = 0
        # aca estoy hardcodeando el stream a las caracteristicas del primer audio
        # probar format = pyaudio.paInt16, channels =2 , rate 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, 
                            channels = 1,
                            rate = 44100,
                            output = True)
        atexit.register(self.close)

    def write_output(self):
        #print(self.START_POINT)
        output = self.frames[self.START_POINT:self.START_POINT+self.CHUNK]
        self.START_POINT += self.CHUNK
        self.stream.write(output)

    def load_file_and_set_frames(self, file_path):
        # agregar excepcion si no lo puede cargar
        self.wf = wave.open(file_path, 'rb')
        self.frames = self.wf.readframes(self.wf.getnframes())
        self.number_of_frames = self.wf.getnframes()

    def close(self):
        self.stream.stop_stream()
        
class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.readPoint.valueChanged.connect(self.readPointValueChanged)
        self.ui.playButton.toggled.connect(self.turnPlayStatusOn)
        self.ui.playButton.setChecked(False)
        self.ui.stopButton.setChecked(True)
        self.status = False 
        self.value = 0
        self.ui.pushButtonLoadFile.clicked.connect(self.openFileDialog)
        self.show()
        self.initAudioPlayer()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.audioCallback)
        self.timer = timer

    def openFileDialog(self):
        self.ui.stopButton.setChecked(True)
        self.status = False
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self, 'Open File','\home','', options = options)
        if fname[0]:
            f = open(fname[0], 'r')
        with f:
            self.player.load_file_and_set_frames(f.name)
            self.player.START_POINT = 0 
            file_name_from_path = f.name.split('/')[-1]
            self.ui.labelFileName.setText(file_name_from_path)
            maximum = int(self.player.number_of_frames / self.player.CHUNK)
            print(maximum)
            self.ui.readPoint.setMaximum(maximum)
            self.ui.readPoint.setValue(0)
            self.timer.start(0.2)

    def readPointValueChanged(self, value):
        self.player.START_POINT = self.player.CHUNK * value
        #print(self.player.START_POINT)

    def turnPlayStatusOn(self, status):
        self.status = self.ui.playButton.isChecked()
        #print(status)
    
    def initAudioPlayer(self):
        self.player = AudioPlayer()
         
    def audioCallback(self):
        if self.status:
            self.player.write_output()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    #w.exec()
    #sys.exit(0)
    sys.exit(app.exec_())


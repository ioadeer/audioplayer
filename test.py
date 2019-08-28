#!/usr/bin/env python3

import sys
import time 
import threading
import pyaudio
import wave
import atexit
from random import randrange
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QTimer
from guiTest1 import *

class AudioPlayer(object):

    def __init__(self):
        self.CHUNK = 8192 #1024 
        self.START_POINT = 0
        #self.wf = wave.open('01_otto_muhl.wav', 'rb')
        self.wf = wave.open('03_Hellucination_1_Drowingirl_mono.wav', 'rb')
        # aca estoy hardcodeando el stream a las caracteristicas del primer audio
        # probar format = pyaudio.paInt16, channels =2 , rate 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),#pyaudio.paInt16,
                            channels = 1,
                            rate = 44100,
                            output = True)
        self.frames = self.wf.readframes(self.wf.getnframes())
        self.number_of_frames = self.wf.getnframes()
        atexit.register(self.close)

    def write_output(self):
        #print(self.START_POINT)
        output = self.frames[self.START_POINT:self.START_POINT+self.CHUNK]
        self.START_POINT += self.CHUNK
        self.stream.write(output)

    def close(self):
        self.stream.stop_stream()
        
class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.readPoint.valueChanged.connect(self.readPointValueChanged)
        self.ui.playSound.toggled.connect(self.turnPlayStatusOn)
        self.ui.playSound.setChecked(True)
        self.status =True 
        self.value = 0
        self.show()
        self.initAudioPlayer()
        maximum = int(self.player.number_of_frames / self.player.CHUNK)
        self.ui.readPoint.setMaximum(maximum)
        timer = QtCore.QTimer()
        timer.timeout.connect(self.audioCallback)
        timer.start(0.2)
        self.timer = timer

    def readPointValueChanged(self, value):
        self.player.START_POINT = self.player.CHUNK * value
        #print(self.player.START_POINT)

    def turnPlayStatusOn(self, status):
        self.status = self.ui.playSound.isChecked()
        #print(status)
    
    def initAudioPlayer(self):
        self.player = AudioPlayer()
         
    def audioCallback(self):
        if self.status:
            self.player.write_output()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyForm()
    w.exec()
    sys.exit(0)


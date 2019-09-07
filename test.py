#!/usr/bin/env python3

import sys
import os
import time 
import pyaudio
import wave
import atexit
import glob
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

    def loadAudioFile(self, f, file_name):
        file_name = f.name.split('/')[-1]
        self.player.load_file_and_set_frames(f.name)
        self.player.START_POINT = 0 
        self.ui.labelFileName.setText(file_name)
        maximum = int(self.player.number_of_frames / self.player.CHUNK)
        self.ui.readPoint.setMaximum(maximum)
        self.ui.readPoint.setValue(0)
        self.timer.start(0.2)
    
    def loadCsvFiles(self, path_of_file, file_name):
        # se podria agregar regular expressions para que levante el formato audo_file_name_frameSize_n_hopSize_n
        csv_files_array = glob.glob(os.path.join(path_of_file,'*.csv'))
        # check if csv file name is equal to wav file name
        clean_csv_files = []
        if csv_files_array:
            for csv_file in csv_files_array:
                #the name of the csv file contains: name of audio file, frame size and hop size
                # in the format audio_file_name_frameSize_n_hopSize_n
                # aca si el csv no contiene la palabra frameSize o hopSize no deberia ser valido
                csv_file_name  = csv_file.split('/')[-1].split('.')[0]
                csv_file_name_list  = csv_file_name.split('_')
                audio_file_name =  csv_file_name.split('frameSize')[0][:-1]
                csv_dict = {
                        'name': audio_file_name,
                        'frameSize':int(csv_file_name_list[csv_file_name_list.index('frameSize')+1]),
                        'hopsize': int(csv_file_name_list[csv_file_name_list.index('hopSize')+1]),
                        }
                print(csv_dict)
        else:
            print('no csv on directory')
        # chequear si csv son resultados de analisis de los audios
        # haciendo un test??

    def openFileDialog(self):
        self.ui.stopButton.setChecked(True)
        self.status = False
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self, 'Open File','\home','', options = options)
        if fname[0]:
            f = open(fname[0], 'r')
        with f:
            file_name_and_extension = f.name.split('/')[-1]
            path_of_file = os.path.dirname(os.path.realpath(f.name))
            file_name = file_name_and_extension.split('.')[0]
            extension = file_name_and_extension.split('.')[-1]
            if extension == 'wav':
                self.loadAudioFile(f, file_name_and_extension)
                self.loadCsvFiles(path_of_file, file_name)
            else:
                print("Must be a .wav file")


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


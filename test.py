#!/usr/bin/env python3

import sys
import os
import time 
import pyaudio
import wave
import scipy.io.wavfile as wf
import atexit
import glob
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.QtCore import QTimer
from guiTest1 import *
sys.path.append('.')
from utils import granular_util as gu

from PyQt5.QtCore import pyqtRemoveInputHook
from pdb import set_trace

# para debuggear:
#pyqtRemoveInputHook()
#set_trace()

class AudioPlayer(object):

    def __init__(self):
        self.CHUNK = 8192 #1024 
        self.START_POINT = 0
        self.frames = 0
        self.fileOrderedFrames = 0
        # aca estoy hardcodeando el stream a las caracteristicas del primer audio
        # probar format = pyaudio.paInt16, channels =2 , rate 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, 
                            channels = 1,
                            rate = 44100,
                            output = True)
        atexit.register(self.close)

    def write_output(self):
        output = self.frames[self.START_POINT:self.START_POINT+self.CHUNK]
        self.START_POINT += self.CHUNK
        self.stream.write(output)

    def load_file_and_set_frames(self, file_path):
        # agregar excepcion si no lo puede cargar
        self.wf = wave.open(file_path, 'rb')
        self.frames = self.wf.readframes(self.wf.getnframes())
        self.fileOrderedFrames = self.frames
        self.number_of_frames = self.wf.getnframes()
        rate, self.sample_array = wf.read(file_path)

    def close(self):
        self.stream.stop_stream()
        
class DataManager(object):

    """Esta clase la estoy implementando para guardar informacion util como
    directorio donde trabajo, para poder cargar archivos csv dinamicamente al
    momemnto de elegir el tamanio de grano ya que cargar todos los csv ocupa
    mucha memoria. tambien quiero hacer aca los procesos de filtrado de data
    frames y calculo de pca"""

    def __init__(self):
        # aca junto los features filtrados
        self.dfs = []
        self.data_file_dict = {}

    def setWorkingDirectory(self, path):
        self.workingDirectory = path

    def loadCsvFiles(self, frameSizeUserInput):
        #pyqtRemoveInputHook()
        #set_trace()
        csv_files_paths_array = glob.glob(os.path.join(self.workingDirectory,'*.csv'))
        if csv_files_paths_array:
            for csv_file_path in csv_files_paths_array:
                #the name of the csv file contains: name of audio file, frame size and hop size
                # in the format audio_file_name_frameSize_n_hopSize_n
                csv_file_name  = csv_file_path.split('/')[-1].split('.')[0]
                csv_file_name_list  = csv_file_name.split('_')
                frameSize = int(csv_file_name_list[csv_file_name_list.index('frameSize')+1])
                if frameSize == frameSizeUserInput:
                    df = pd.read_csv(csv_file_path)
                    audio_file_name =  csv_file_name.split('frameSize')[0][:-1]
                    self.data_file_dict = {
                            'name': audio_file_name,
                            'frameSize': frameSize,
                            'hopSize': int(csv_file_name_list[csv_file_name_list.index('hopSize')+1]),
                            'data_frame': df,
                            }
        else:
            print('no csv on directory')
    
    def filter_data_frame(self, data_frame, columns):
        #pyqtRemoveInputHook()
        #set_trace()                  
        self.filteredDataFrame = self.data_file_dict['data_frame'].filter(items=columns)

    def performPCA(self):
        x = StandardScaler().fit_transform(self.filteredDataFrame)
        pca = PCA(n_components =2)
        principalComponents = pca.fit_transform(x)
        tempDf = []
        principalDf = pd.DataFrame(data = principalComponents,
                                    columns = ['principal component 1',
                                        'principal component 2'])
        tempDf.append(principalDf)
        tempDf.append(self.filteredDataFrame)
        self.filteredDataFrame =pd.concat(tempDf, axis= 1)
        


class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.readPoint.valueChanged.connect(self.readPointValueChanged)
        self.ui.playButton.toggled.connect(self.turnPlayStatusOn)
        self.ui.playButton.setChecked(False)
        self.ui.stopButton.setChecked(True)
        self.ui.comboBoxGrainSize.currentIndexChanged.connect(self.reload_features)
        self.ui.listWidgetFeatures.itemSelectionChanged.connect(self.set_selected_features)
        self.ui.pushButtonFilterFeatures.clicked.connect(self.filter_features)
        self.ui.pushButtonRearrange.clicked.connect(self.rearrange_frames)
        self.ui.pushButtonPerformPCA.clicked.connect(self.call_pca)
        self.ui.pushButtonOriginalOrder.clicked.connect(self.arrange_frames_original_order)
        self.status = False 
        self.value = 0
        self.ui.pushButtonLoadFile.clicked.connect(self.openFileDialog)
        self.show()
        self.initAudioPlayer()
        self.initDataManager()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.audioCallback)
        self.timer = timer

    def loadAudioFile(self, f, file_name):
        file_name = f.name.split('/')[-1]
        self.player.load_file_and_set_frames(f.name)
        self.player.START_POINT = 0 
        self.ui.labelFileName.setText(file_name)
        maximum = int(self.player.number_of_frames / self.player.CHUNK)
        #self.ui.readPoint.setSingleStep(self.player.CHUNK)
        self.ui.readPoint.setMaximum(maximum)
        self.ui.readPoint.setValue(0)
        self.timer.start(0.2)

    def openFileDialog(self):
        self.ui.stopButton.setChecked(True)
        self.status = False
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self, 'Open Wav File','\home','', options = options)
        if fname[0]:
            f = open(fname[0], 'r')
        with f:
            file_name_and_extension = f.name.split('/')[-1]
            path_of_file = os.path.dirname(os.path.realpath(f.name))
            file_name = file_name_and_extension.split('.')[0]
            extension = file_name_and_extension.split('.')[-1]
            if extension == 'wav':
                self.loadAudioFile(f, file_name_and_extension)
                self.dataManager.setWorkingDirectory(path_of_file)
                self.dataManager.loadCsvFiles(int(self.ui.comboBoxGrainSize.itemText(self.ui.comboBoxGrainSize.currentIndex())))
                self.loadAllFeaturesToFeatureListWidget()
            else:
                print("Must be a .wav file")


    def initAudioPlayer(self):
        self.player = AudioPlayer()

    def initDataManager(self):
        self.dataManager = DataManager()

    def readPointValueChanged(self, value):
        # se agrego el * 2 por el stereo
        self.player.START_POINT = self.player.CHUNK * value * 2 

    def turnPlayStatusOn(self, status):
        self.status = self.ui.playButton.isChecked()
         
    def audioCallback(self):
        if self.status:
            self.player.write_output()

    def loadAllFeaturesToFeatureListWidget(self):
        self.ui.listWidgetFeatures.clear()
        self.ui.listWidgetFeatures.addItems(self.dataManager.data_file_dict['data_frame'].columns.values[1:])

    def reload_features(self):
        self.dataManager.loadCsvFiles(int(self.ui.comboBoxGrainSize.itemText(self.ui.comboBoxGrainSize.currentIndex())))
        self.loadAllFeaturesToFeatureListWidget()

    def set_selected_features(self):
        self.ui.listWidgetSelectedFeatures.clear()
        selectedFeatures = self.ui.listWidgetFeatures.selectedItems()
        for i in list(selectedFeatures):
            self.ui.listWidgetSelectedFeatures.addItem(i.text())

    def addSelectedFeaturesToComboBox(self, items_string_array):
        self.ui.comboBoxGrainSortingCriterion.clear()
        self.ui.comboBoxGrainSortingCriterion.addItems(items_string_array)

    def filter_features(self):
        if self.ui.listWidgetSelectedFeatures.count() > 0:
            tempFeatureStringArray = [self.ui.listWidgetSelectedFeatures.item(i).text() for i in range(self.ui.listWidgetSelectedFeatures.count())]
            self.dataManager.filter_data_frame(self.dataManager.data_file_dict['data_frame'], tempFeatureStringArray) 
            self.addSelectedFeaturesToComboBox(tempFeatureStringArray)
        else:
            print("No features selected")
    
    def rearrange_frames(self):
        # para detener audio callback function
        #self.status = False
        if self.ui.comboBoxGrainSortingCriterion.count() > 0:
            featureValues = np.array(self.dataManager.filteredDataFrame[self.ui.comboBoxGrainSortingCriterion.currentText()].values)
            featureValuesSorted= np.argsort(featureValues)
            windowType = self.ui.comboBoxWindowType.currentText()
            # pyaudio.paInt16
            #samples = np.frombuffer(self.player.fileOrderedFrames, dtype= np.int16)
            samples_rearranged = gu.rearrange(self.dataManager.data_file_dict['frameSize'],
                                                self.dataManager.data_file_dict['hopSize'],
                                                self.player.sample_array,
                                                featureValuesSorted,
                                                windowType)
            rearrenged_bytes = samples_rearranged.astype(np.int16).tobytes() 
            self.status = False
            self.player.frames = rearrenged_bytes
            self.status = True

    def call_pca(self):
        if self.ui.listWidgetSelectedFeatures.count() > 0:
            self.dataManager.performPCA()
            #pyqtRemoveInputHook()
            #set_trace()
            tempFeatureStringArray = self.dataManager.filteredDataFrame.columns.values[:]
            self.ui.listWidgetFeatures.addItems(tempFeatureStringArray)
            self.addSelectedFeaturesToComboBox(tempFeatureStringArray)
        else:
            print('select and filter features to perform pca')

    def arrange_frames_original_order(self):
        self.player.frames = self.player.fileOrderedFrames


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())


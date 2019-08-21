#!/usr/bin/env python3

import sys
import time 
import threading
import pyaudio
import wave
from random import randrange
from PyQt5.QtWidgets import QApplication, QDialog
from guiTest1 import *

#CHUNK = 1024
#CHUNK = 512
CHUNK = 8192 
#CHUNK = 16384
exitFlag = 0
START_POINT= 0
status= True
readPoint = 0
#class Ui_Dialog(QMainWindow):
class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.readPoint.valueChanged.connect(self.readPointValueChanged)
        self.ui.playSound.toggled.connect(self.turnPlayStatusOn)
        self.status =True 
        self.value = 0
        self.show()

    def readPointValueChanged(self, value):
        self.value = value
        #print(value)

    def turnPlayStatusOn(self, status):
        self.status = self.ui.playSound.isChecked()
        #print(status)

    def getValue(self):
        return self.value
    def getSatus(self):
        return self.status

class playAudio(threading.Thread):
    global CHUNK    
    global status
    def __init__(self):
        threading.Thread.__init__(self)
        self.CHUNK = CHUNK
        self.start_point  = 0
        #self.START_POINT = START_POINT
    def run(self):
        global START_POINT
        global status
        global readPoint
        wf = wave.open('01_otto_muhl.wav', 'rb')
        #wf = wave.open('example.wav', 'rb')
        #wf = wave.open('03_Hellucination_1_Drowingirl_mono.wav', 'rb')
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels= wf.getnchannels(),
                        rate= wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)
        nframes = wf.getnframes()
        frames = wf.readframes(wf.getnframes())
        #output = frames[START_POINT:CHUNK+START_POINT] 
        print("status before audio"+str(status))
        while(status):
        #for i in range (250):
            threadLock.acquire()
            #print("Global status on audio thread"+str(status))
            #print("Start Point in audio thread: "+str(START_POINT))
            start_point = START_POINT
            #print("read point"+str(readPoint))
            #print("start_point"+str(start_point))
            output = frames[START_POINT:CHUNK+START_POINT+1] 
            #output = frames[start_point:CHUNK+start_point] 
            #print("output frames "+str(output))
            #while len(output) > 0:
            for j in range(25):  #aumentar o disminuir para tamanio d grano
                stream.write(output)
                START_POINT += CHUNK
                output = frames[START_POINT:START_POINT+CHUNK]
            threadLock.release()
            time.sleep(0.01)
        else:
            print("no audio")
            time.sleep(0.1)
        print("eof") 
        #time.sleep(1)
        stream.stop_stream()
        stream.close()
        print("Exit thread")

class myThread(threading.Thread):
    global CHUNK
    def __init__(self, w, Toggle):
        
        threading.Thread.__init__(self)
        self.w = w
        self.status = False
        self.toggle = Toggle
    def run(self):
        print("Starting "+self.name)
        global START_POINT
        global status
        global readPoint
        #self.status = self.toggle.playSound.isChecked()
        #status =  True
        time.sleep(0.1)
        while(True):
            threadLock.acquire()
            status = self.w.getSatus()
            #print("Status on Gui thread"+str(status))
            readPoint = self.w.getValue()
            #print("From fader "+ str(readPoint))
            START_POINT = CHUNK * readPoint 
            #print("STart point at myThread "+str(START_POINT))
            threadLock.release()
            time.sleep(0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyForm()
    p = pyaudio.PyAudio()
    threadLock = threading.Lock()
    thread2 = myThread(w, w.ui.readPoint)
    thread1 = playAudio()
    thread2.start()
    thread1.start()
    w.exec()
    thread1.join()
    thread2.join()
    p.terminate()
    sys.exit(0)


# Granular synthesis util module

import numpy as np


def envelopeWindow(windowSize, windowType):
    '''
    este metodo devuelve la envolvente de una ventana de análisis normalizada
    en forma de numpy array de tamaño windowSize y de tipo windowType que puede ser
    'hanning', 'hamming, 'blackman', 'gaussian', 'welch' y 'bartlett', TODO:
    agregar expodec y rexpodec'''

    lookUp = np.zeros(windowSize)
    for i in range(windowSize):
        lookUp[i] = ((i/ (windowSize/2)) -1) * np.pi
    windowFunction = {
        'hanning': lambda x: 0.5 + 0.5 * np.cos(x),
        'hamming': lambda x: 0.54 + 0.46 * np.cos(x),
        'blackman': lambda x: 0.42 + 0.5 * np.cos(x) + 0.08 * np.cos(2*x),
        'gaussian': lambda x: (-1 * (x **2) + 10)/10,
        'welch' : lambda x: ((1 - x ** 2) + 10)/10,
        'bartlett': lambda x: 1 - abs(x),
    }
    return windowFunction[windowType](lookUp)


def rearrange(windowFrameSize, hopSize, audioData, rearrangeIndex, windowEnvType):
    #create arrays
    '''
    este método toma un numpy array que contiene valores de muestras de audio
    (audioData) y devuelve otro numpy array que también representa una lista de
    samples pero reordenados según el criterio rearrangeIndex'''

    nHops = windowFrameSize/hopSize
    env = envelopeWindow(windowFrameSize, windowEnvType)
    sampleArrays = np.zeros((int(nHops), len(audioData)))
    for idx, i in enumerate(rearrangeIndex):
       chunkStart = i * hopSize 
       chunkEnd = chunkStart + windowFrameSize
       if(chunkEnd < len(audioData)):
           chunk = audioData[chunkStart:chunkEnd]
           #apply env
           chunk = np.multiply(chunk, env)
           assignLookUp = idx * hopSize
           n = int((assignLookUp % windowFrameSize) / hopSize)
           if(assignLookUp + windowFrameSize < sampleArrays.shape[1]):
               sampleArrays[n, assignLookUp: assignLookUp+windowFrameSize] = chunk[:]
    output = sampleArrays.sum(axis=0)
    return output

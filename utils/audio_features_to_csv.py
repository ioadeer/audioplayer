#!/usr/bin/env python3

""" 
Extraer infromación de audio volcarlo a csv. Hacer análisis de acuerdo con
tamaño de ventana de análisis dado ( frameSize) , y con hopSize determinado que
idealmente sea 1/4 del tamaño de frameSize.  
"""

#import essentia.standard as es
import pandas as pd
import numpy as np
import getopt
import sys
import os


def usage():
    print("Script to extract lowlevel features info from a sound file and export it to a csv file")
    print("Example: python audio_features_to_csv.py -f <file_name> --framesize=<framesize> --hopsize=<hopsize>")
    print("<framesize> should be a power of 2. <hopsize> should be smaller than framesize. freamesize/4 = hopsize is an ideal value")

def main():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'f:h',['help','framesize=','hopsize='])  # 'f:h' tienen que estar en orden alfabetico
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    filepath = None
    frameSize = None
    hopSize = None

    if len(opts) != 0:
        for (o,a) in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit(2)
            elif o in ('-f'):
                filepath = a
            elif o in ('--framesize'):
                frameSize = int(a)
            elif o in ('--hopsize'):
                hopSize= int(a)
            else:
                print("fin de switch")
                usage()
                sys.exit(2),
    else:
        # no options passed
        usage()
        sys.exit(2)

    if frameSize and hopSize and filepath:
        import essentia.standard as es
        # Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame features
        features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                                      rhythmStats=['mean', 'stdev'],
                                                      mfccStats=['mean'],
                                                      lowlevelFrameSize= frameSize,
                                                      lowlevelHopSize= hopSize,
                                                      tonalStats=['mean', 'stdev'])(filepath)
        dfs = []
        
        for idx, name in enumerate(features_frames.descriptorNames()):
            if name.startswith('lowlevel'):
                feature_name = name.rsplit('.')[1]
                if isinstance(features_frames[name], np.ndarray):
                    if features_frames[name].ndim ==1:
                        columns = [feature_name]
                    else:
                        columns = [feature_name+'_'+str(i) for i in range(features_frames[name].shape[1])]
                    dfs.append(pd.DataFrame(features_frames[name], columns=columns))
        
        df = pd.concat(dfs,axis=1)
        
        file_name = features['metadata.tags.file_name'].rsplit('.')[0]
        name = file_name.replace(' ', '_')+'_frameSize_'+str(frameSize)+'_hopSize_'+str(hopSize)+'.csv'
        base_dir = os.getcwd()
        df.to_csv(os.path.join(base_dir,name))
    else:
        usage()
        sys.exit(2)


if __name__ == "__main__":
    main() 

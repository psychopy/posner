from os import path
from psychopy import misc, gui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#choose some data files to analyse
filenames = gui.fileOpenDlg(allowed="*.csv")

#loop through the files
for thisFilename in filenames:
    print thisFilename
    thisDat = pd.read_csv(thisFilename)
    
    #filter out bad data
    filtered = thisDat[ thisDat['rt']<=1.0 ]
    filtered = filtered[ filtered['corr']==1 ]
    
    #separate conflicting from congruent reaction times
    conflict = filtered[filtered.description == 'conflict']
    congruent = filtered[filtered.description != 'conflict']
    #get mean/std.dev
    meanConfl = np.mean(conflict.rt)
    semConfl = np.std(conflict.rt, ddof=1)
    meanCongr = np.mean(congruent.rt)
    semCongr = np.std(congruent.rt, ddof=1)
    fig, ax = plt.subplots(1)
    ax.bar([1,2], [meanConfl, meanCongr], yerr=[semConfl, semCongr])
    plt.show()
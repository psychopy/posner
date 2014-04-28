from os import path
from psychopy import misc, gui
import pandas as pd
import scipy
from scipy import stats

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
    meanConfl = scipy.mean(conflict.rt)
    semConfl = scipy.std(conflict.rt, ddof=1)
    meanCongr = scipy.mean(congruent.rt)
    semCongr = scipy.std(congruent.rt, ddof=1)
    print "Conflict = %.3f (std=%.3f)" %(meanConfl, semConfl)
    print "Congruent = %.3f (std=%.3f)" %(meanCongr, semCongr)
    
    #run a t-test
    t, p = stats.ttest_ind(conflict.rt, congruent.rt)
    print "Independent samples t-test: t=%.3f, p=%.4f" %(t, p)

    # Create a Figure:
    fig, ax = plt.subplots(1)
    ax.bar([1,2], [meanConfl, meanCongr], yerr=[semConfl, semCongr])
    plt.show()
    
    
    

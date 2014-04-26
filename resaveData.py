"""This is not a particularly useful example of saving out
csv files from a set of psydat files
"""
from os import path
from psychopy import misc, gui

#select some files to use
filenames = gui.fileOpenDlg(allowed="*.psydat")

#loop through the files
for thisFilename in filenames:
    #get a new name
    fileNoExt, fileExt = path.splitext(thisFilename)
    newName = fileNoExt+"NEW.csv"
    #load and save
    dat = misc.fromFile(thisFilename)
    dat.saveAsWideText(newName)
    print 'saved', newName
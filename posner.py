# Import psychopy modules
from psychopy import visual, core, event, data, gui, logging

# Toggle debugging/production
DEBUG = True
if DEBUG:
    fullscr = False
    logging.console.setLevel(logging.DEBUG)
else:
    fullscr = True
    logging.console.setLevel(logging.WARNING)

# Collect general parameters in the "info" dictionary
info = {} #a dictionary
#present dialog to collect info
info['participant'] = ''
dlg = gui.DlgFromDict(info)
if not dlg.OK:
    core.quit()
#add additional info after the dialog has gone
info['fixFrames'] = 30 #0.5s at 60Hz
info['cueFrames'] = 12 #200ms at 60Hz
info['probeFrames'] = 12
info['dateStr'] = data.getDateStr() #will create str of current date/time

#create the base filename for our data files
filename = "data/{participant}_{dateStr}".format(**info)
logfile = logging.LogFile(filename+".log",
    filemode='w',#if you set this to 'a' it will append instead of overwriting
    level=logging.EXP)

# initialise stimuli
win = visual.Window([1024,768], fullscr=fullscr, monitor='testMonitor', units='deg')
fixation = visual.Circle(win, size = 0.5,
    lineColor = 'white', fillColor = 'lightGrey')
probe = visual.ImageStim(win, size = 2, # 'size' is 3xSD for gauss,
    pos = [5, 0], #we'll change this later
    image = None, mask = 'gauss',
    color = 'green')
cue = visual.ShapeStim(win, 
    vertices = [[-3,-2], [-3,2], [3,0]],
    lineColor = 'red', fillColor = 'salmon')
respClock = core.Clock()

# Run a block of trials. nReps is a positive integer and saveTrial is True/False.
def runBlock(nReps, saveTrials=True):
    #set up the trials/experiment
    conditions = data.importConditions('conditions.csv') #import conditions from file
    trials = data.TrialHandler(trialList=conditions, nReps=nReps) #create trial handler (loop)
    #add trials to the experiment handler to store data
    if saveTrials:
        thisExp = data.ExperimentHandler(
                name='Posner', version='1.0', #not needed, just handy
                extraInfo = info, #the info we created earlier
                dataFileName = filename, # using our string with data/name_date
                )
        thisExp.addLoop(trials) #there could be other loops (like practice loop)
    
    # Actually present stimuli: loop through trials
    for thisTrial in trials:
        
        # set up this trial
        resp = None
        rt = None
        probe.setPos( [thisTrial['probeX'], 0] )
        cue.setOri( thisTrial['cueOri'] )
        
        #fixation period
        fixation.setAutoDraw(True)
        for frameN in range(info['fixFrames']):
            win.flip()
            
        #present cue
        cue.setAutoDraw(True)
        for frameN in range(info['cueFrames']):
            win.flip()
        cue.setAutoDraw(False)
    
        #present probe and collect responses during presentation
        probe.setAutoDraw(True)
        win.callOnFlip(respClock.reset) #NB: reset not reset()
        event.clearEvents()
        for frameN in range(info['probeFrames']):
            keys = event.getKeys(keyList = ['left','right','escape'])
            if len(keys)>0:
                resp = keys[0] #take the first keypress as the response
                rt = respClock.getTime()
                break #out of the probe-drawing loop
            win.flip()
        probe.setAutoDraw(False)
        fixation.setAutoDraw(False)
        
        #clear screen
        win.flip()
        
        #wait for response if we didn't already have one
        if resp is None:
            keys = event.waitKeys(keyList = ['left','right','escape'])
            resp = keys[0] #take first response
            rt = respClock.getTime()
        
        #check if the response was correct
        if thisTrial['probeX']>0 and resp=='right':
            corr = 1
        elif thisTrial['probeX']<0 and resp=='left':
            corr = 1
        elif resp=='escape':
            corr = None
            trials.finished = True
        else:
            corr = 0
        
        
        #store the response and RT
        trials.addData('resp', resp)
        trials.addData('rt', rt)
        trials.addData('corr', corr)
    
        # Register end of trial in the log file
        if saveTrials:
            thisExp.nextEntry()

runBlock(1, saveTrials=False)
runBlock(5)
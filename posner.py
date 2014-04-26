from psychopy import visual, core, event, data, gui

info = {} #a dictionary
#present dialog to collect info
info['participant'] = ''
dlg = gui.DlgFromDict(info)
if not dlg.OK:
    core.quit()
#add additional info after the dialog has gone
info['fixTime'] = 0.5 # seconds
info['cueTime'] = 0.2
info['probeTime'] = 0.2
info['dateStr'] = data.getDateStr() #will create str of current date/time
#create the base filename for our data files
filename = "data/{participant}_{dateStr}".format(**info)

win = visual.Window([1024,768], fullscr=False, units='pix')

# initialise stimuli
fixation = visual.Circle(win, size = 5,
    lineColor = 'white', fillColor = 'lightGrey')
probe = visual.ImageStim(win, size = 80, # 'size' is 3xSD for gauss,
    pos = [300, 0], #we'll change this later
    image = None, mask = 'gauss',
    color = 'green')
cue = visual.ShapeStim(win, 
    vertices = [[-30,-20], [-30,20], [30,0]],
    lineColor = 'red', fillColor = 'salmon')

#set up the trials/experiment
conditions = data.importConditions('conditions.csv') #import conditions from file
trials = data.TrialHandler(trialList=conditions, nReps=5) #create trial handler (loop)

#add trials to the experiment handler to store data
thisExp = data.ExperimentHandler(
        name='Posner', version='1.0', #not needed, just handy
        extraInfo = info, #the info we created earlier
        dataFileName = filename, # using our string with data/name_date
        )
thisExp.addLoop(trials) #there could be other loops (like practice loop)

respClock = core.Clock()
for thisTrial in trials:
    # set up this trial
    probe.setPos( [thisTrial['probeX'], 0] )
    cue.setOri( thisTrial['cueOri'] )
    #fixation period
    fixation.draw()
    win.flip()
    core.wait(info['fixTime'])
    #present cue
    cue.draw()
    win.flip()
    core.wait(info['cueTime'])
    #present probe
    fixation.draw()
    probe.draw()
    win.flip()
    respClock.reset()
    core.wait(info['probeTime'])
    
    #clear screen
    win.flip()
    
    #wait for response
    keys = event.waitKeys(keyList = ['left','right','escape'])
    resp = keys[0] #take first response
    rt = respClock.getTime()
    
    #check if the response was correct
    if thisTrial['probeX']>0 and resp=='right':
        corr = 1
    elif thisTrial['probeX']<0 and resp=='left':
        corr = 1
    elif resp=='escape':
        trials.finished = True
    else:
        corr = 0
    #store the response and RT
    trials.addData('resp', resp)
    trials.addData('rt', rt)
    trials.addData('corr', corr)
    thisExp.nextEntry()
        

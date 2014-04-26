from psychopy import visual, core, event, data

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

# run one trial
fixation.draw()
win.flip()
cue.draw()
win.flip()
probe.draw()
win.flip()

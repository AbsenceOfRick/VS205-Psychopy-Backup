#!/usr/bin/env python
from psychopy import *
import numpy
import random
import scipy
import matplotlib as mplot
import matplotlib.mlab as mlab
import matplotlib.pyplot as pyplot

def myshuf(lis):
	for i in range(len(lis)):
		idx = int( scipy.rand() * (len(lis)-(i+1)) )
		t = lis[i+idx]
		lis[i+idx] = lis[i]
		lis[i] = t
	return lis

ab_time = 1.000
noise_time = 0.020

isi_time = 1.0

backcon = 0.0

#change_contrast = False
#timed_contrast = 0.53
#stimvals = [ 0.0, 0.1, 0.2, 0.30, 0.5 ]
#noise_time = 0.050

change_contrast = True # change contrast? (else time)
#stimvals = [ 0.52, 0.53, 0.55, 0.6 ]

# 1 = all white, 128 = at background, 255 = all black
stimvals = [ 110, 121, 122, 124, 126 ]

# Subj 1 AB, subj 2 AB, subj 3 AB, etc.
resp_keys = numpy.array( ['a','s', 'v','b', 'k', 'l'] )
trial_time = 0.500

stimreps = 5

#stimvals = numpy.linspace(0.51,0.59,5)
#stimvals = [0.51, 0.53, 0.54, 0.545, 0.55]
num_observers = 3

num_stims = len(stimvals)
max_trials = num_stims * stimreps
trial_seq = myshuf( numpy.tile( stimvals, (1,stimreps) )[0] )
results = numpy.zeros( (num_observers, max_trials) )


#create a window to draw in
#myWin = visual.Window((800,600), allowGUI=True, fullscr=True)
myWin = visual.Window((800,600), fullscr=False, color=numpy.tile( backcon, 3) )
trial_inA = [random.random() < 0.5 for i in numpy.arange(len(trial_seq))]

#INITIALISE SOME STIMULI
fixSpot = visual.PatchStim(myWin,tex="sin", sf=20.0, pos=(0.1,0.00), size=(0.02,0.02), rgb=[0.1,0.1,0.1] )

noise = visual.PatchStim( myWin, tex="none", pos=(-0.005, -0.01), size=(0.1,0.1), rgb=[0.8,0.8,0.8] )

grating = visual.PatchStim(myWin,pos=(0.0,0.0),
                           tex="sin",#mask="gauss",
                           rgb=[1.0,1.0,1.0],
                           size=(2.0,2.0), sf=10.0)

myMouse = event.Mouse(win=myWin)
#message = visual.TextStim(myWin,pos=(-0.95,-0.95),alignHoriz='right',height=0.08, text='left-drag=SF, right-drag=pos, scroll=ori')
#message = visual.TextStim(myWin,pos=(-0.95,-0.9),alignHoriz='left',height=0.08,
    #text='left-drag=SF, right-drag=pos, scroll=ori')
		# update the text display if it changes
message = visual.TextStim(myWin,pos=(0.0,0.0),
		alignHoriz='left',height=0.04, ori=00, text='C', font='Sloan',
		color=(0.59,0.59,0.59))

message2 = visual.TextStim(myWin,pos=(0.0,0.7),
		alignHoriz='left',height=0.10, ori=00, text='C', 
		color=(1.00,1.00,1.00))

mess_on = True
quit = 0

message.setText('Get ready!')
message.draw()
myWin.flip()
event.waitKeys()

info_csf = {'spatial_freq':10,
	'contrast':0,
	'distance_cm':56,
	'screen_width_cm':19.3675,
	'coarse_inc':0.1,
	'fine_inc':0.001}

info_tmtf = {'freq':10,
	'screen_refresh':120,
	'coarse_inc':0.1,
	'fine_inc':0.001,
	'mean_luminance':0.25}

tmtf_mod = 0.25
tmtf_phase = 0
tmtf_phase_inc = 0.25

tmtf_mode = False
csf_mode = False

def adjust(up, fine):
	global tmtf_mod
	if tmtf_mode:
		if up:
			mult = 1.0
		else:
			mult = -1.0

		if fine:
			tmtf_mod += mult*info_tmtf['fine_inc']
		else:
			tmtf_mod += mult*info_tmtf['coarse_inc']

	else: # csv mode
		if up:
			mult = 1.0
		else:
			mult = -1.0

		if fine:
			grating.setContrast(mult*info_csf['fine_inc'],'+')
		else:
			grating.setContrast(mult*info_csf['coarse_inc'],'+')

def setTrialText( mess, which):
    if which:
	    #mess.setText('C   O')
	    mess.setText('C')
    else:
	    mess.setText('O')
	    #mess.setText('O   C')

trial = 0
while trial < max_trials: #continue until keypress

    # Set the contrast
    if change_contrast:
        #message.setColor( numpy.tile( trial_seq[trial], (1,3) )[0] )
        message.setColor(int(trial_seq[trial]) , 'rgb255')
        on_time = trial_time
    else:
        message.setColor( numpy.tile(timed_contrast, 3) )
        on_time = trial_seq[trial]

    setTrialText( message, trial_inA[trial] )

    message.draw()
    myWin.flip()
    core.wait(on_time)

    if noise_time > 0:
        noise.setTex( scipy.rand( 128,128) ) 
        noise.draw()
        fixSpot.draw()
        myWin.flip()
        core.wait(noise_time)

    setTrialText( message, not trial_inA[trial] )

    myWin.flip()
    core.wait(ab_time)

    message.draw()
    myWin.flip()
    core.wait(on_time)

    if noise_time > 0:
        noise.setTex( scipy.rand( 128,128) ) 
        noise.draw()
        fixSpot.draw()
        myWin.flip()
        core.wait(noise_time)

    myWin.flip()

    resps = numpy.zeros( num_observers ) == 1.0
    while len(mlab.find(resps)) < num_observers:
        for key in event.getKeys():

         if key in ['up']:
             trial_seq[trial] += 1
             #fixSpot.setColor(int(trial_seq[trial]) , 'rgb255')
             #fixSpot.draw()
             message.setColor(int(trial_seq[trial]) , 'rgb255')
             message.draw()
             myWin.flip()

         if key in ['down']:
           trial_seq[trial] -= 1
           #fixSpot.setColor(int(trial_seq[trial]) , 'rgb255')
           #ixSpot.draw()
           message.setColor(int(trial_seq[trial]) , 'rgb255')
           message.draw()
           myWin.flip()

         if key in ['d']:
              #message2.setColor( tile( 1.0, (1,3) )[0] )
              message2.setText( 'val=%f' % trial_seq[trial] )
              #message.setFont('Times')
              message2.draw()
              myWin.flip()
              #event.waitKeys()
              #message.setFont('Sloan')

         if key in ['escape','q']:
              myWin.close()
              trial = max_trials
              resps = numpy.zeros( num_observers ) == 0.0

              break

         if key in resp_keys: #['a', 's']: #resp_keys2:
              #print 'hi'
              #obs = 
              #resps[0] = True
              #resps[1] = True
              #esps[2] = True
              #esults[0][0]= 1
              #idx = fi
              (obs,idx) = divmod( mlab.find( resp_keys == key )[0], 2) #2=2afc
              resps[obs] = True
              results[obs, trial] = idx
              #resp = mod( find( resp_
				
        #if key in ['d']:
            #mess_on = not mess_on

        #if key in ['r']:
            #message.ori = numpy.mod(message.ori + 90, 360)
        #if key in ['comma']:

    trial += 1

    #core.wait(isi_time)
    noise.setSize( (0.01, 0.01) )
    noise.setTex( -1.0 - numpy.zeros( (4,4) ) )
    noise.draw()
    myWin.flip()
    core.wait(isi_time)
    noise.setSize( (0.1, 0.1) )
    #if isi_time > 0:
        #noise.setTex( scipy.rand( 256,256) ) 
        #noise.draw()
        #fixSpot.draw()
        #myWin.flip()
        #core.wait(isi_time)

for which_trial in numpy.arange(max_trials):
	trial_correct = [ trial_inA != results[subj, :] for subj in numpy.arange(num_observers) ]

#for which_stim in arange(num_stims):
	#stimidxs = mlab.find( trial_seq==stimvals[which_stim] )
	#for subj in arange(num_observers):
		#stimcorrect = results[subj, stimidxs] == 

tots = [ [len( mlab.find((trial_seq == stimvals[trial]) & trial_correct[subj]) )
	for trial in numpy.arange(num_stims)] for subj in numpy.arange(num_observers) ]

pyplot.figure()
for i in numpy.arange(num_observers):
	pyplot.subplot(3,1,i+1)
	pyplot.plot( stimvals, numpy.array(tots[i]) / float(stimreps), 'o-' )
	pyplot.ylim( 0-0.1,1.0+0.1 )
	pyplot.title( '%i' % i)
	pyplot.grid()
	#pyplot.legend( ['%i' % i for i in arange(num_observers)] )

pyplot.show()

#done = False
#while not done:
	#if 'q' in event.getKeys():
		#done = True
	#if 'escape' in event.getKeys():
		#done = True

myWin.close()

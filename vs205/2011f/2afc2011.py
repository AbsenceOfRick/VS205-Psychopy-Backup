#!/usr/bin/env python
import numpy as np
from psychopy import *
import numpy
import time
import matplotlib.pyplot as pyplot
import numpy.random

# for our monitors: contr=100%, bright=50%
rslope = 2.201
gslope = 2.473
bslope = 2.055
vda = 9156 # empirical: mean of values after 50

backsteal = 768 #768

def abslum( (r,g,b) ):
	return ((r**rslope+g**gslope+b**rslope))/vda

def gentable2( r ):
	vals = np.zeros( len(r) * 6 )
	coords = np.zeros( (len(r) * 6,3) )
	count = 0
	for baseval in r:
		for (r,g,b) in ([-1,-1,0], [0,-1,0], [0,-1,1], [-1,0,-1], [-1,0,0], [0,0,0] ):
				coords[count] = [baseval+r, baseval+g, baseval+b ]
				#vals[count] = abslum( (baseval+r, baseval+g, baseval+b )	 )
				vals[count] = abslum( coords[count] )
				count += 1
	withkeys = numpy.array([ (val,n) for n,val in enumerate(vals) ], [('val',float), ('idx', int) ] )
	#return sort( withkeys, order='val' )
	return withkeys,coords

def possible(r):
	poss = gentable2( r )
	figure();
	plot( np.arange(len(r)* 6), poss['val'], 'k.-' )
	for n,val in enumerate(r):
		plot( [0,len(r)*6], np.tile(abslum( (val,val,val ) ),2), 'b--' )	
	
steallum = gentable2( np.arange(255) )[0]['val']
stealcoords = gentable2( np.arange(255) )[1]

fullscr = True  # make sure this matches next
screendim = (1024,768)
screensize = 100.0 / 36.0 # pix/cm for Sony Trinitron
distance = 600.0 # mm
fixation_text='+'

SubjectName = 'dc2' 
num_observers = 2

continc = [1,0,0]
backcol = (stealcoords[backsteal] -127.0)/128.0#[0,0,0]

# Set up the screen, etc.
myWin = visual.Window(screendim, allowGUI=True, color=backcol, units='pix', fullscr=fullscr )
myWin.setMouseVisible(False)

abloc=100

framec = 75
displaytext = visual.TextStim(myWin,pos=(0,200),alignHoriz='center', height=9, font='Arial' ) 
#quare = visual.ShapeStim(myWin,pos=(0,0), vertices=((-90,-90), (-90,90), (90,90), (90,-90) ), lineColor=backcol ) 
theframeA = visual.ShapeStim(myWin,pos=(-abloc,0),vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor="white", fillColor=None )
theframeB = visual.ShapeStim(myWin,pos=(abloc,0),vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor="white", fillColor=None )
ee   = visual.TextStim(myWin,pos=(-abloc,0), color=backcol, height=100, text="E")
eeB = visual.TextStim(myWin,pos=( abloc,0), color=backcol, height=100, text="E")
count = visual.TextStim(myWin,pos=(0,200), color=(-1,-1,-1), height=20, text="ready")

done = False
display=False

ontime = 0.035
offtime = 0.400
counttime = 0.225

message  = visual.TextStim(myWin,pos=(-200,140), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))
message0 = visual.TextStim(myWin,pos=(-200,220), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))
message1 = visual.TextStim(myWin,pos=(-200,200), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))
message2 = visual.TextStim(myWin,pos=(-200,180), alignHoriz='left',height=16, ori=00, color=(-1.00,-1.00,-1.00))

message0.setText("Subject 1: 'a' = Yes/First interval, 's'=No/Second interval.")
message1.setText("Subject 2: 'v' = Yes/First interval, 'b'=No/Second interval.")
message2.setText("Subject 3: 'k' = Yes/First interval, 'l'=No/Second interval.")

messageA = visual.TextStim(myWin,pos=(-abloc,140), alignHoriz='left',height=20, ori=00, color=(-1.00,-1.00,-1.00), text="A")
messageB = visual.TextStim(myWin,pos=( abloc,140), alignHoriz='left',height=20, ori=00, color=(-1.00,-1.00,-1.00), text="B")

#ee.setColor( "#%02X%02X%02X" % (200,200,200) )
#theframe.draw()
#ee.draw()
#myWin.flip()
#core.wait(ontime)
whitesteal = 200*6

message0.draw()
if num_observers>1:
	message1.draw()
if num_observers>2:
	message2.draw()

message.setText("The first trial will be a test trial. Do you see the white flashed 'E' inside the box? Press any key to start.")
message.draw()
myWin.flip()
event.waitKeys()
message.setText("")

stimvals = numpy.array([ 0, 2, 4, 8, 16, 32]) + backsteal
stimreps = 8
trialseq = numpy.random.permutation( numpy.tile( stimvals, stimreps) )
trialseq = numpy.concatenate( ([whitesteal], trialseq) ) # put a high-contrast demo trial

maxtrials = len(trialseq)

trial_inA = numpy.random.permutation( numpy.tile( numpy.array([True,False]), (maxtrials-1)/2.0 ) )
trial_inA = numpy.concatenate( ([True],trial_inA) )

#rgb = numpy.array([100,100,100])
stolen = backsteal # start at 127,127,127 (= background) # start at this

resp_keys = numpy.array( ['a','s', 'v','b', 'k', 'l'] )


results = numpy.zeros( (num_observers, maxtrials) )

trial = 0

# Main loop
while not done:
	stolen = trialseq[trial]

	#quare.setFillColor( "#%02X%02X%02X" % (rgb[0],rgb[1], rgb[2]) )
	#quare.draw()
 	count.draw()
 	myWin.flip()
	core.wait(counttime)
 	#count.setText('1')
 	#count.draw()
 	#myWin.flip()
	#core.wait(counttime)

	#theframe.draw()
	#myWin.flip()
	#core.wait(counttime)
	if trial_inA[trial]:
		rgb = stealcoords[stolen]
		rgbB = stealcoords[backsteal]
	else:
		rgb = stealcoords[backsteal]
		rgbB = stealcoords[stolen]

	ee.setColor( "#%02X%02X%02X" % (rgb[0],rgb[1], rgb[2]) )
	eeB.setColor( "#%02X%02X%02X" % (rgbB[0],rgbB[1], rgbB[2]) )
	theframeA.draw()
	theframeB.draw()
	ee.draw()
	eeB.draw()
	messageA.draw()
	messageB.draw()
	myWin.flip()
	core.wait(ontime)

	if display:
		displaytext.setText( "bak=%s stealidx=%d steallum=%f rgb=%s" % ( str(backcol),stolen, steallum[stolen], str(rgb) ) )
		displaytext.draw()

	#ee.draw() # REMOVE ME for short duration
#	theframe.draw()
	#message.draw()
	message0.draw()
	if num_observers>1:
		message1.draw()
	if num_observers>2:
		message2.draw()
	myWin.flip()
	core.wait(offtime)

	#for key in event.waitKeys():
	gotall=False
	resps = numpy.tile( False, num_observers)
	while not gotall:
		for key in event.getKeys():
			if key in [ 'escape', 'q' ]:
				done = True
			elif key in [ 'down' ]:
				stolen -= continc[0]
			elif key in [ 'up' ]:
				stolen += continc[0]
			elif key in [ 'r' ]:
				repeat = (repeat == False)
			elif key in [ '0' ] :
				key = '10'
			elif key in [ 'quoteleft']:
				key = '0'
			elif key in [ 'd']:
				display = (display==False)
			elif key in resp_keys:
				(obs,idx) = divmod( numpy.where( resp_keys == key )[0][0], 2)
				resps[obs] = True
				results[obs, trial] = idx
				gotall = all(resps)

			if not resps[0]:
				message0.draw()
			if num_observers>1:
				if not resps[1]:
					message1.draw()
				if num_observers>2:
					if not resps[2]:
						message2.draw()
			myWin.flip()
				
	trial += 1
	if trial==maxtrials:
		done=True
    
# Post process: collate and display
#for which_trial in numpy.arange(max_trials):
trial_correct = numpy.array([ (trial_inA==(results[subj]==0)) for subj in numpy.arange(num_observers) ])

#for which_stim in arange(num_stims):
    #stimidxs = mlab.find( trial_seq==stimvals[which_stim] )
    #for subj in arange(num_observers):
        #stimcorrect = results[subj, stimidxs] == 

tots = [ [len( numpy.where( numpy.all( (trialseq==stim,trial_correct[subj]),0))[0]) for stim in stimvals] for subj in numpy.arange(num_observers) ]

myWin.setMouseVisible(True)
pyplot.figure()
for i in numpy.arange(num_observers):
    pyplot.subplot(3,1,i+1)
    #pyplot.plot( stimvals, numpy.array(tots[i]) / float(stimreps), 'o-' )
    pyplot.plot( [(abslum(coord)-abslum(stealcoords[backsteal]))/abslum(stealcoords[backsteal]) for coord in stealcoords[stimvals]], numpy.array(tots[i]) / float(stimreps), 'o-' )
    #pyplot.xticks( numpy.arange(len(stimvals)), [str('%.2f') % (abslum(coord)-abslum(stealcoords[backsteal])) for coord in stealcoords[stimvals]] ) 
    pyplot.title( 'Subject %i' % (i+1))
    pyplot.grid()
    pyplot.semilogx()
    pyplot.ylim( 0-0.1,1.0+0.1 )
   #pyplot.legend( ['%i' % i for i in numpy.arange(num_observers)] )

pyplot.show()

myWin.close()

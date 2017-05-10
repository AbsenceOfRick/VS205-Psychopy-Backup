#!/usr/bin/env python
import numpy as np
from psychopy import *
import numpy
import time
import matplotlib.pyplot as pyplot

# for our monitors:
rslope = 2.201
gslope = 2.473
bslope = 2.055
vda = 9156 # empirical: mean of values after 50

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

fullscr = True # make sure this matches next
screendim = (1024,768)
screensize = 100.0 / 36.0 # pix/cm for Sony Trinitron
distance = 600.0 # mm
fixation_text='+'

SubjectName = 'dc2' 

continc = [1,0,0]
backcol = [0,0,0]

# Set up the screen, etc.
myWin = visual.Window(screendim, allowGUI=True, color=backcol, units='pix', fullscr=fullscr )
myWin.setMouseVisible(False)

framec = 75
displaytext = visual.TextStim(myWin,pos=(0,200),alignHoriz='center', height=9, font='Arial' ) 
#quare = visual.ShapeStim(myWin,pos=(0,0), vertices=((-90,-90), (-90,90), (90,90), (90,-90) ), lineColor=backcol ) 
theframe = visual.ShapeStim(myWin,vertices=((-framec,-framec), (-framec,framec), (framec,framec), (framec,-framec) ), lineColor="white" )
ee = visual.TextStim(myWin,pos=(0,0), color=backcol, height=100, text="E")
count = visual.TextStim(myWin,pos=(0,200), color=(1,1,1), height=100, text="2")

done = False
display=False

ontime = 0.030
offtime = 0.270
counttime = 0.250

#rgb = numpy.array([100,100,100])
stolen = 768 # start at 127,127,127 (= background)
# Main loop
while not done:

	rgb = stealcoords[stolen]
	#quare.setFillColor( "#%02X%02X%02X" % (rgb[0],rgb[1], rgb[2]) )
	#quare.draw()
	#count.setText('2')
 	#count.draw()
 	#myWin.flip()
	#core.wait(counttime)
 	#count.setText('1')
 	#count.draw()
 	#myWin.flip()
	#core.wait(counttime)

	#theframe.draw()
	#myWin.flip()
	#core.wait(counttime)

	ee.setColor( "#%02X%02X%02X" % (rgb[0],rgb[1], rgb[2]) )
	theframe.draw()
	ee.draw()
	if display:
		displaytext.setText( "bak=%s stealidx=%d steallum=%f rgb=%s" % ( str(backcol),stolen, steallum[stolen], str(rgb) ) )
		displaytext.draw()

	myWin.flip()
	core.wait(ontime)

	if display:
		displaytext.setText( "bak=%s stealidx=%d steallum=%f rgb=%s" % ( str(backcol),stolen, steallum[stolen], str(rgb) ) )
		displaytext.draw()

	#ee.draw() # REMOVE ME for short duration
#	theframe.draw()
	myWin.flip()
	#core.wait(offtime)


	for key in event.waitKeys():
	#for key in event.getKeys():
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
            

    
myWin.close()

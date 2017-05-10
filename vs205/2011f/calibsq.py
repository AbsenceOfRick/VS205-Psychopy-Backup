#!/usr/bin/env python
from psychopy import *
import numpy
import time
import matplotlib.pyplot as pyplot

fullscr = True # make sure this matches next
screendim = (1024,768)
screensize = 100.0 / 36.0 # pix/cm for Sony Trinitron
distance = 600.0 # mm
fixation_text='+'

SubjectName = 'dc' 

continc = numpy.array([.0,.0, .0])
backcol = numpy.array([ 0, 0, 0])

# Set up the screen, etc.
myWin = visual.Window(screendim, allowGUI=True, color=backcol, units='pix', fullscr=fullscr )
myWin.setMouseVisible(False)

sqrad = 100
displaytext = visual.TextStim(myWin,pos=(0,300),alignHoriz='center', height=9, font='Arial', color=-1.0 ) 
square = visual.ShapeStim(myWin,pos=(0,0), vertices=((-sqrad,-sqrad), (-sqrad,sqrad), (sqrad,sqrad), (sqrad,-sqrad) ), lineColor=backcol ) 
#square = visual.TextStim(myWin,pos=(0,0), color=[-1,-1,-1], height=40, text='E', font='Arial' ) 

done = False
display=False

rgb = numpy.array([0, 0, 0])
# Main loop
while not done:

	square.setFillColor( "#%02X%02X%02X" % (rgb[0],rgb[1], rgb[2]) )
	square.draw()
	if display:
		displaytext.setText( 'tgt: %s bak: %s' % ( str(rgb), str(backcol) ) )
		displaytext.draw()

	myWin.flip()

	for key in event.getKeys():
		if key in [ 'escape', 'q' ]:
			done = True
		elif key in [ 'down' ]:
			rgb -= continc
		elif key in [ 'up' ]:
			rgb += continc
		elif key in [ 'left' ]:
			backcol -= continc/255.0
			#myWin.setColor( "#%02X%02X%02X" % (backcol[0],backcol[1], backcol[2]) )
			myWin.setColor(  backcol ) #, colorSpace='rgb255')
		elif key in [ 'right' ]:
			backcol += continc/255.0
			#myWin.setColor( "#%02X%02X%02X" % (backcol[0],backcol[1], backcol[2]) )
			myWin.setColor(  backcol) #/255.0, colorSpace='rgb255')
		elif key in [ 'r' ]:
			repeat = (repeat == False)
		elif key in [ '0' ] :
			key = '10'
		elif key in [ 'quoteleft']:
			key = '0'
		elif key in [ 'd']:
			display = (display==False)

myWin.close()

#!/usr/bin/env python
from psychopy import *
import numpy
"""
As of version 1.51 the mouse coordinates for
    myMouse.getPos()
    myMouse.setPos() #pygame only
    myMouse.getRel()
are in the same units as the window.

You can also check the motion of the wheel with myMouse.getWheelRel() 
(in two directions for the mac mighty mouse or equivalent!)
"""
#create a window to draw in
#myWin = visual.Window((800,600), allowGUI=True, fullscr=True)
myWin = visual.Window((800,600))

#INITIALISE SOME STIMULI
#fixSpot = visual.PatchStim(myWin,tex="none", mask="gauss",pos=(0,0), size=(0.05,0.05),rgb=[-1.0,-1.0,-1.0])
grating = visual.PatchStim(myWin,pos=(0.0,0.0),
                           tex="sin",#mask="gauss",
                           rgb=[1.0,1.0,1.0],
                           size=(2.0,2.0), sf=10.0)
myMouse = event.Mouse(win=myWin)
#message = visual.TextStim(myWin,pos=(-0.95,-0.95),alignHoriz='right',height=0.08, text='left-drag=SF, right-drag=pos, scroll=ori')
#message = visual.TextStim(myWin,pos=(-0.95,-0.9),alignHoriz='left',height=0.08,
    #text='left-drag=SF, right-drag=pos, scroll=ori')
		# update the text display if it changes
message = visual.TextStim(myWin,pos=(0.4,0.5),alignHoriz='left',height=0.08, text=str(grating.sf[0]))

mess_on = True

info_csf = {'spatial_freq':10,
	'contrast':0,
	'distance_cm':56,
	'screen_width_cm':19.3675,
	'coarse_inc':0.1,
	'fine_inc':0.001}

while True: #continue until keypress
    #handle key presses each frame
    for key in event.getKeys():
        if key in ['escape','q']:
            core.quit()

        if key in ['c']:
            dlg = gui.DlgFromDict(info_csf)
            if dlg.OK:
                screen_degs = numpy.arctan(info_csf['screen_width_cm']/info_csf['distance_cm'])*180.0/numpy.pi

                print screen_degs
                print info_csf['spatial_freq']*screen_degs
                grating.setSF(info_csf['spatial_freq']*screen_degs)
                grating.setContrast(info_csf['contrast'])

        if key in ['d']:
            mess_on = not mess_on

        if key in ['u','4']:
            grating.setContrast(info_csf['fine_inc'],'+')
        if key in ['m','0']:
            grating.setContrast(-info_csf['fine_inc'],'+')
        if key in ['i','5']:
            grating.setContrast(info_csf['coarse_inc'],'+')
        if key in ['comma']:
            grating.setContrast(-info_csf['coarse_inc'],'+')
        if key in ['k']:
            grating.setContrast(0)
	
            
    #get mouse events
    mouse_dX,mouse_dY = myMouse.getRel()
    mouse1, mouse2, mouse3 = myMouse.getPressed()
    if (mouse1):
        grating.setSF(mouse_dX, '+')

    elif (mouse3):
        grating.setPos([mouse_dX, mouse_dY], '+')
        
    #Handle the wheel(s):
    # Y is the normal mouse wheel, but some (e.g. mighty mouse) have an x as well
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    grating.setOri(wheel_dY*5, '+')
    
    event.clearEvents()#get rid of other, unprocessed events
    
    #do the drawing
    #fixSpot.draw()
    #grating.setPhase(0.05, '+')#advance 0.05cycles per frame
    grating.draw()

    if mess_on:
        message.setText('Contrast=%f'%grating.contrast)
        message.draw()

    myWin.flip()#redraw the buffer


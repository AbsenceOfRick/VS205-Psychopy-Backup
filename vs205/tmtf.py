#!/usr/bin/env python
from psychopy import *
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
myWin = visual.Window((600.0,600.0), allowGUI=True)

#INITIALISE SOME STIMULI
fixSpot = visual.PatchStim(myWin,tex="none", mask="gauss",pos=(0,0), size=(0.05,0.05),rgb=[-1.0,-1.0,-1.0])
fixSpot = visual.PatchStim(myWin,tex="none", mask="gauss",pos=(0,0), size=(100,100),rgb=[0.2,0.2,0.2])
grating = visual.PatchStim(myWin,pos=(0.1,0.1),
                           tex="sin",mask="gauss",
                           rgb=[0.1,0.1,0.1],
                           size=(10.0,10.0), sf=(2,0))
myMouse = event.Mouse(win=myWin)
message = visual.TextStim(myWin,pos=(1.1,1.1),alignHoriz='left',height=0.08, text='left-drag=SF, right-drag=pos, scroll=ori')

mess_on = False

tmtf_phase = 0
tmtf_phase_inc = 0.1

while True: #continue until keypress
    #handle key presses each frame
    for key in event.getKeys():
        if key in ['escape','q']:
            core.quit()
        else:
            if mess_on:
                mess_on = False
            else:
                mess_on = True

#message = visual.TextStim(myWin,pos=(-0.95,-0.9),alignHoriz='left',height=0.08,
    #text='left-drag=SF, right-drag=pos, scroll=ori')
            
    #get mouse events
    mouse_dX,mouse_dY = myMouse.getRel()
    mouse1, mouse2, mouse3 = myMouse.getPressed()
    if (mouse1):
        grating.setSF(mouse_dX, '+')

		# update the text display if it changes
        message = visual.TextStim(myWin,pos=(0.5,0.5),alignHoriz='left',height=0.08, text=str(grating.sf[0]))
    elif (mouse3):
        grating.setPos([mouse_dX, mouse_dY], '+')
        
    #Handle the wheel(s):
    # Y is the normal mouse wheel, but some (e.g. mighty mouse) have an x as well
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    grating.setOri(wheel_dY*5, '+')
    
    event.clearEvents()#get rid of other, unprocessed events

    if tmtf_phase < 0.5: #numpy.pi:
        fixSpot.setContrast(0.8)
    else:
        fixSpot.setContrast(0.9)
        if tmtf_phase >= 1.0: #2*numpy.pi:
			tmtf_phase = 0.0 - tmtf_phase_inc
    tmtf_phase += tmtf_phase_inc

    fixSpot.draw()

    message = visual.TextStim(myWin,pos=(0.5,0.5),alignHoriz='left',height=0.08,
text=str(fixSpot.contrast))
    
    #do the drawing
    #fixSpot.draw()
    #grating.setPhase(0.00, '+')#advance 0.05cycles per frame
    #grating.draw()

    if mess_on:
        message.draw()

    myWin.flip()#redraw the buffer


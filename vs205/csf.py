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
myWin = visual.Window((1024,768), allowGUI=False)
myWin.setMouseVisible(False)

#INITIALISE SOME STIMULI
fixSpot = visual.PatchStim(myWin,tex="none", pos=(0,0), size=(2.00,2.00),rgb=[1.0,1.0,1.0])

grating = visual.PatchStim(myWin,pos=(0.0,0.0),
                           tex="sin", mask="gauss",
                           rgb=[1.0,1.0,1.0],
                           size=(2.0,2.0), sf=10.0)
myMouse = event.Mouse(win=myWin)
#message = visual.TextStim(myWin,pos=(-0.95,-0.95),alignHoriz='right',height=0.08, text='left-drag=SF, right-drag=pos, scroll=ori')
#message = visual.TextStim(myWin,pos=(-0.95,-0.9),alignHoriz='left',height=0.08,
    #text='left-drag=SF, right-drag=pos, scroll=ori')
		# update the text display if it changes
message = visual.TextStim(myWin,pos=(0.25,0.6),alignHoriz='left',height=0.08, text=str(grating.sf[0]))

mess_on = True

info_csf = {'spatial_freq':5,
        'contrast':0.0,
        'distance_cm':70.0,
        'screen_width_cm':31.0,
        'coarse_inc':0.001,
        'fine_inc':0.0001}

info_tmtf = {'freq':10,
        'screen_refresh':85.0,
        'coarse_inc':0.001,
        'fine_inc':0.0001,
	'mean_luminance':0.25}

tmtf_mod = 0.25
tmtf_phase = 0
tmtf_phase_inc = 0.25

tmtf_mode = False

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

tmtf_mode = False
dlg = gui.DlgFromDict(info_csf)
screen_degs = numpy.arctan(info_csf['screen_width_cm']/info_csf['distance_cm'])*180.0/numpy.pi
while True: #continue until keypress
    #handle key presses each frame
    #get mouse events
    mouse_dX,mouse_dY = myMouse.getRel()
    info_csf['contrast'] += mouse_dY
    #print mouse_dY
    grating.setSF(info_csf['spatial_freq']*screen_degs)
    grating.setContrast( (info_csf['contrast'] / 2.0 * 1.20) )
    tmtf_mod += mouse_dY * 1.0
    if (tmtf_mod) < 0:
        tmtf_mod = 0
    if ( info_csf['contrast'] < 0):
        info_csf['contrast'] = 0
    for key in event.getKeys():
        if key in ['escape','q']:
            core.quit()

        if key in ['t']:
            tmtf_mode = True
            dlg = gui.DlgFromDict(info_tmtf)
            if dlg.OK:
                tmtf_phase_inc = float(info_tmtf['freq'])/info_tmtf['screen_refresh']
                print tmtf_phase_inc

        if key in ['s']:
            tmtf_mode = False
            dlg = gui.DlgFromDict(info_csf)
            if dlg.OK:
                screen_degs = numpy.arctan(info_csf['screen_width_cm']/info_csf['distance_cm'])*180.0/numpy.pi

                #print screen_degs
                #print info_csf['spatial_freq']*screen_degs
                grating.setSF(info_csf['spatial_freq']*screen_degs)
                grating.setContrast(info_csf['contrast'])

        if key in ['d']:
            mess_on = not mess_on

        if key in ['up']:
           if tmtf_mode:
               info_tmtf['freq'] *= 2
               tmtf_phase_inc = float(info_tmtf['freq'])/info_tmtf['screen_refresh']
           else:
               info_csf['spatial_freq'] *= 2.0
               grating.setSF(info_csf['spatial_freq']*screen_degs)
        if key in ['down']:
           if tmtf_mode:
               info_tmtf['freq'] *= 0.5
               tmtf_phase_inc = float(info_tmtf['freq'])/info_tmtf['screen_refresh']
           else:
               info_csf['spatial_freq'] *= 0.5
               grating.setSF(info_csf['spatial_freq']*screen_degs)
        if key in ['u','4']:
            adjust(True,True)

        if key in ['m','0']:
            adjust(False,True)
        if key in ['i','5']:
            adjust(True,False)
            #grating.setContrast(info_csf['coarse_inc'],'+')
        if key in ['comma']:
            adjust(False,False)
            #grating.setContrast(-info_csf['coarse_inc'],'+')
        if key in ['k']:
            if tmtf_mode:
                tmtf_mod = 0.0
            else:
                grating.setContrast(0)

    if tmtf_mode:
        if tmtf_phase < 0.5: #numpy.pi:
            fixSpot.setContrast(numpy.sin(tmtf_phase*numpy.pi*2.0)*tmtf_mod
                + info_tmtf['mean_luminance'])
        else:
            fixSpot.setContrast(numpy.sin(tmtf_phase*numpy.pi*2.0)*tmtf_mod
                + info_tmtf['mean_luminance'])

            if tmtf_phase >= 1.0: #2*numpy.pi:
			    tmtf_phase -= 1.0

        tmtf_phase += tmtf_phase_inc
        fixSpot.draw()
    else:
        grating.draw()

    if mess_on:
        if tmtf_mode:
            message.setText('contrast=%f\nfreq=%f'%
                (tmtf_mod, info_tmtf['freq']) )
        else:
            message.setText('contrast=%f\nfreq=%f'%
                (grating.contrast, info_csf['spatial_freq']) )

        message.draw()

    myWin.flip()#redraw the buffer

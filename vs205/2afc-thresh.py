#!/usr/bin/env python

# Timing parameters:
ab_time = 1.000
noise_time = 0.000
isi_time = 1.0
trial_time = 0.300

# Stimulus/background parameters:
stimvals = [ 154, 155, 157 ,160, 164, 170 ]
stimreps = 8
backconf = 0.2
backcon = -1.0 # the real background RGBs
pedconf = 0.2
targ_text = 'C'
fix_contrast = -0.15

# Experimental conditions:
change_contrast = True # change contrast? (else time)
pretrial_fix = True
condition = 3
ascend = False
descend = False

# I/O and misc parameters:
output_graph = True
output_hits = False

execfile('common.py')

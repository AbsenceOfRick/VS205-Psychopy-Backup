#!/usr/bin/env python

# Timing parameters:
ab_time = 1.000
noise_time = 0.000
isi_time = 1.0
trial_time = 0.300

# Stimulus/background parameters:
stimvals = [ 152, 152, 154, 156, 157, 160 ]
stimreps = 5
backconf = 0.2
backcon = 0.0
pedconf = 0.2
targ_text = 'C'
fix_contrast = -0.15

# Experimental conditions:
change_contrast = True # change contrast? (else time)
pretrial_fix = True
condition = 1
ascend = False
descend = False

# I/O and misc parameters:
output_graph = False
output_hits = True

execfile('common.py')

#!/usr/bin/env python
import numpy

# Timing parameters:
ab_time = 1.000
noise_time = 0.000
isi_time = 1.0
trial_time = 0.350

# Stimulus/background parameters:
stimvals = numpy.arange(20)+152
stimreps = 1
backconf = 0.2
backcon = 0.0
pedconf = 0.2
targ_text = 'C'
fix_contrast = -0.15

# Experimental conditions:
change_contrast = True # change contrast? (else time)
pretrial_fix = True
condition = 1
ascend = True
descend = False

# I/O and misc parameters:
output_graph = False
output_hits = False

execfile('common.py')

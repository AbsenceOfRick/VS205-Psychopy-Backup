#!/usr/bin/env python

# Timing parameters:
ab_time = 1.000
noise_time = 0.200
pre_noise_time = 0.200
isi_time = 1.0
trial_time = 0.200
fix_time = 0.3

# Stimulus/background parameters:
stimvals = [ 152, 152, 154, 156, 157, 160 ]
stimreps = 5
backconf = 0.0
backcon = -1.0
pedconf = 0.0
targ_text = '.'
fix_contrast = -0.15
pedsize=(0.3,0.3)
targheight = 0.2 # 0.04 orig
targpos=(-targheight/10,targheight/3)

# Experimental conditions:
change_contrast = True # change contrast? (else time)
pretrial_fix = False
fixation_big_cross = True
condition = 2
ascend = False
descend = False
method_adj = True
targInc = 1.00 # doesn't yet work since trial_seq is int

# I/O and misc parameters:
output_graph = False
output_hits = True
dmesgColor = (200,100,100) 

execfile('common.py')

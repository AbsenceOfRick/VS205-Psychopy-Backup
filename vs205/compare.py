def read_single(filename, numrows=26, numcols=26):
	global line, line_fields, result, numread
	result = zeros ( (numcols, numrows ))
	file = open(filename, 'rt')
	numread=0
	while file:
		line = file.readline()
		if len(line) == 0:
			break
		line_fields = line.strip().split(',')
		result[numread] = line_fields
		numread += 1
	return result

def outputjsx(freq, arr, file):
	outfile = open(filename, 'wt')
	
	output.writelines('var dataArr = [')
	
	for item in freq:
		output.writelines("%f," % item)

	output.writelines('], [')
	for item in freq:
		output.writelines("%f," % item)

	output.writelines(']];\n')
	

def show_calib():
	global calib_steps, calib_vals

	calib_steps = read_single('calib1k.txt',1,25 )
	calib_vals = read_single('calib1v.txt',1,25 )

	figure();
	subplot(1,2,1)
	plot( log10(calib_steps), log10(calib_vals),'o-' ); grid()
	subplot(1,2,2)
	plot( (calib_steps), (calib_vals),'o-' ); grid()
	#millilamberts?
	#figure(); plot( (calib_steps), log10(calib_vals/3.183),'o-' ); grid()

def interp( vals, steps, x):
	idx = where( steps >= x  )[0][0] - 1
	y = vals[idx] + (x-steps[idx]) * ((vals[idx+1] - vals[idx]) / (steps[idx+1]-steps[idx]) )
	return y


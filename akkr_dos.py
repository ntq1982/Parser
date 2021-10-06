#!/usr/bin/env python3

'''

	Get density of states from AkaiKKR calculation

	Copyright (C) 2021 Quang Nguyen. All rights reserved.
	Created on Sep 28, 2021 at Osaka University
	Last modified: Oct 06, 2021 20:00 JST

'''

import math
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser

# Get input arguments
parser = OptionParser()
parser.add_option("-i", "--input", dest="file",
			action="store", type="string", help="Input file containing DOS")
parser.add_option("-p", "--plot", dest="plot",
			action="store_true", help="Plot the total DOS")
parser.add_option("-t", "--total", dest="tdos",
			action="store_true", help="Extract the total DOS")
parser.add_option("-a", "--atmid", dest="index",
			action="store", type="int", help="Extract the partial DOS")
(options, args) = parser.parse_args()

# Check input arguments
if (not options.file):
	print("ERROR: No input file provided!")
	print("Use option '-h' or '--help' for details.")
	exit()
else:
	if (not options.plot) and (not options.tdos) and (options.index is None):
		print("ERROR: One more option should be provide!")
		print("Use option '-h' or '--help' for details.")
		exit()
if (options.plot):
	yes_plot = True
	str_tdos = 'total DOS'
else:
	yes_plot = False
if (options.tdos):
	yes_tdos = True
	str_tdos = 'total DOS'
else:
	yes_tdos = False
if (options.index is not None):
	if (options.index <= 0):
		print("ERROR: Atomic index should be positive!")
		exit()
	yes_pdos = True
	str_pdos = 'DOS of component'
else:
	yes_pdos = False

# Parse DOS from file
str_magtyp = 'magtyp'
str_mse = 'mse'
data_tdos = []
data_pdos = []
component = 0
with open(options.file, mode='r') as infile:
	for line in infile:
		if str_magtyp in line:
			value = line.strip(' \n').split('=')[1]
			if value == 'nmag':
				ispin = 1
			else:
				ispin = 2
		if str_mse in line:
			next_line = infile.readline()
			size = [int(i) for i in next_line.split()]
			mse = size[1]
		if yes_plot or yes_tdos:
			if str_tdos in line:
				for i in range(mse - 1):
					data_tdos.append(infile.readline().strip('\n'))
		if yes_pdos:
			if str_pdos in line:
				component += 1
				if (component == options.index):
					for i in range(mse - 1):
						data_pdos.append(infile.readline().strip('\n'))

# Plot total DOS
if yes_plot:
	en = np.empty(0)
	tdos = tdos1 = tdos2 = np.empty(0)
	for i in range(mse - 1):
		en = np.append(en, np.array(float(data_tdos[i].strip().split()[0])))
		if ispin == 1:
			tdos = np.append(tdos, np.array(float(data_tdos[i].strip().split()[1])))
		else:
			tdos1 = np.append(tdos1, np.array(float(data_tdos[i].strip().split()[1])))
			tdos2 = np.append(tdos2, np.array(float(data_tdos[i].strip().split()[2])))
	plt.xlim([en[0], en[-1]])
	if ispin == 1:
		plt.ylim([0.0, 1.2 * np.amax(tdos)])
		plt.axvline(x=0.0, linewidth=0.5, color='k', linestyle='--')
		plt.plot(en, tdos, linewidth=1, linestyle='-', color='r', label='Total DOS')
	else:
		plt.ylim([1.2 * np.amin(-tdos2), 1.2 * np.amax(tdos1)])
		plt.axvline(x=0.0, linewidth=0.5, color='k', linestyle='--')
		plt.axhline(y=0.0, linewidth=0.5, color='k', linestyle='-')
		plt.plot(en, tdos1, linewidth=1, linestyle='-', color='r', label='Total DOS')
		plt.plot(en, -tdos2, linewidth=1, linestyle='-', color='r', label=None)
	plt.xlabel("$E - E_{F}$ (Ry)")
	plt.ylabel("$DOS$ (1/Ry/Vcell)")
	plt.legend(loc='best', shadow=True)
	plt.show()

# Save DOS to file
if yes_tdos:
	with open("tdos.dat", mode='w') as outfile:
		print("{:1s} {:>11s} {:>12s}"
			.format('#', 'Energy(Ry)', 'DOS(1/Ry/Vc)'), file=outfile)
		for i in range(mse - 1):
			print(data_tdos[i], file=outfile)
if yes_pdos:
	with open("pdos"+str(options.index)+".dat", mode='w') as outfile:
		print("{:1s} {:>10s} {:>24s}"
			.format('#', 'Energy(Ry)', 'DOS(1/Ry/Vc): s p d...'), file=outfile)
		for i in range(mse - 1):
			print(data_pdos[i], file=outfile)
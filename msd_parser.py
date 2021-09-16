#!/usr/bin/env python3

'''

   Parsing data from PHONOPY's thermal_displacements.yaml

   Copyright (C) 2021 Quang Nguyen. All rights reserved
   Created on Sep 16, 2021 at Osaka University
   Last modified: Sep 16, 2021 17:35 JST

'''

import math, yaml

with open('thermal_displacements.yaml') as file:
	data = yaml.load(file, Loader=yaml.FullLoader)

natom = data['natom']
print('{:>18s} {}'.format('Number of atoms:', natom))

ntemp = 0
for x in data:
	if isinstance(data[x], list):
		ntemp += len(data[x])
print("{:>25s} {}".format('Number of temperatures:', ntemp))

for i in range(natom):
	print('{:23s} {} {:1s}'.format('\n  Displacements of atom', i + 1, ':'))
	print("{:>16s} {:>16s} {:>16s} {:>16s} {:>16s}".format('Temperature[K]',
		'X-Displ[Å^2]', 'Y-Displ[Å^2]', 'Z-Displ[Å^2]', 'Tot_Displ[Å^2]') )
	for j in range(ntemp):
		temp = data['thermal_displacements'][j]['temperature']
		displ = data['thermal_displacements'][j]['displacements'][i]
		total = math.sqrt(displ[0]**2 + displ[1]**2 + displ[2]**2)
		print("{:1s} {:14.3f} {:16.7f} {:16.7f} {:16.7f} {:16.7f}".
			format(' ', temp, *displ, total))

print("\n  Parsed successfully!")
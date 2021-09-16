#!/usr/bin/env python3

'''

   Parsing data from PHONOPY's thermal_displacements.yaml

   Copyright (C) 2021 Quang Nguyen. All rights reserved
   Created on Sep 16, 2021 at Osaka University
   Last modified: Sep 16, 2021 23:04 JST

'''

import yaml

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
	print('{:31s} {} {:1s}'.format('\n  Thermal displacements of atom', i + 1, ':'))
	print("{:>16s} {:>16s} {:>16s} {:>16s} {:>16s}".format('Temperature[K]',
		'MSD_X[Å^2]', 'MSD_Y[Å^2]', 'MSD_Z[Å^2]', 'MSD_Tot[Å^2]') )
	for j in range(ntemp):
		temp = data['thermal_displacements'][j]['temperature']
		msd_xyz = data['thermal_displacements'][j]['displacements'][i]
		msd_tot = msd_xyz[0] + msd_xyz[1] + msd_xyz[2]
		print("{:1s} {:14.3f} {:16.7f} {:16.7f} {:16.7f} {:16.7f}".
			format(' ', temp, *msd_xyz, msd_tot))

print("\n  Parsed successfully!")
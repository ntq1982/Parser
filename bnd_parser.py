#!/usr/bin/env python3

'''

   Parsing data from PHONOPY's band.yaml

   Copyright (C) 2021 Quang Nguyen. All rights reserved
   Created on Sep 20, 2021 at Osaka University
   Last modified: Sep 20, 2021 18:00 JST

'''

import yaml

with open("band.yaml") as file:
	data = yaml.load(file, Loader=yaml.FullLoader)

natom = data['natom']
nqpoint = data['nqpoint']
npath = data['npath']
nband = 3 * natom
print("{:>18s} {}".format('Number of atoms:', natom))
print("{:>18s} {}".format('Number of bands:', nband))
print("{:>21s} {}".format('Number of q-points:', nqpoint))
print("{:>18s} {}".format('Number of paths:', npath))

print("\n  Saving data to band.dat")
with open("band.dat", "w") as fileout:
	print("{:1s} {:>14s} {:>14s} {:>14s} {:>14s} {:>17s}".format('#',
		'Q-PointX', 'Q-PointY', 'Q-PointZ', 'Distance', 'Frequency'), file = fileout)
	for k in range(nband):
		print("{:15s} {}".format('# Band number:', k + 1), file = fileout)
		for i in range(nqpoint):
			qpoint_xyz = data['phonon'][i]['q-position']
			distance = data['phonon'][i]['distance']
			frequency =data['phonon'][i]['band'][k]['frequency']
			print("{:1s} {:14.7f} {:14.7f} {:14.7f} {:14.7f} {:17.10f}"
				.format(' ', *qpoint_xyz, distance, frequency), file = fileout)
		print('', file = fileout)

print("\n  Parsed successfully!")
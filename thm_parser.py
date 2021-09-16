#!/usr/bin/env python3

'''

   Parsing data from PHONOPY's thermal_properties.yaml

   Copyright (C) 2020 Quang Nguyen. All rights reserved
   Created on Oct 07, 2020 at Osaka University
   Last modified: Sep 16, 2021 19:06 JST

'''

import yaml

with open("thermal_properties.yaml") as file:
	data = yaml.load(file, Loader = yaml.FullLoader)

ndata = 0
for x in data:
	if isinstance(data[x], list):
		ndata += len(data[x])
print("{:>24s} {}".format('Number of data points:', ndata))

print ("{:>13s} {:>13s} {:>13s}".format('\n  Temperature', 'Entropy', 'Free-Energy'))
for i in range(ndata):
	temperature = data['thermal_properties'][i]['temperature']
	free_energy = data['thermal_properties'][i]['free_energy']
	entropy = data['thermal_properties'][i]['entropy']
	heat_capacity = data['thermal_properties'][i]['heat_capacity']
	energy = data['thermal_properties'][i]['energy']
	print ("{:13.3f} {:13.7f} {:13.7f}".format(temperature, entropy, free_energy))

print("\n  Parsed successfully!")
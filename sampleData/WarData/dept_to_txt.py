# -*- coding:utf-8 -*-
import json
import numpy as np
from collections import defaultdict
import pprint

x = []
time_window = 600000
max_time_block = -999
max_time = 10
id_Core = np.zeros((max_time,1000,1000),dtype=np.float64)

with open("data.txt") as outfile: 
	for index, l in enumerate(outfile):
		from_id,to_id,time = l.strip().split(" ")

		time_block = int(time)/time_window
		
		if time_block > max_time: 	
			break

		id_Core[int(time_block), int(from_id),int(to_id)] += 1 
		
		if max_time_block < time_block:
			max_time_block = time_block



print max_time_block, "time"

outfile = open('data.npy','w')
np.save(outfile, id_Core)
outfile.close()

#out = open('roi_eu_core_ids.txt', 'w')
#for index, author in enumerate(range(90)):
#	out.write(str(index).encode('utf8')+'\n')
#out.close()

#out = open('roi_time_manual.txt', 'w')
#for index in range(0,max_time_block,1): 
#	out.write(str(index).encode('utf8')+'\n')
#out.close()


# -*- coding:utf-8 -*-
import json
import numpy as np
from collections import defaultdict
import pprint

x = []
time_window = 100000
max_time_block = -999
max_time = 80

counter = 0 
		
# Require Manual intervention 
denomintor = 100000
Offset = 1084585996

#289
totalTimeSteps = 200
# 1495092000000
stopTime = Offset * denomintor + (totalTimeSteps * 18 * denomintor)
print stopTime

time1 = set()
time_block = 0
last_block = 0

from1 = -1
to1 = -1

with open("fbForum.txt") as outfile: 
	for index, l in enumerate(outfile):
			from_id,to_id,time = l.strip().split(",")
			time_block = int(time)/time_window
			time1.add(time_block)

			if from1< from_id:
				from1 = from_id
				print from1, "from"
			
			if to1 < to_id:
				to1 = to_id
				print to1, "to"

			if time_block > max_time: 	
				print "What",  time_block, index
				break

			if max_time_block < time_block:
				max_time_block = time_block

print from1,to1, "asd"

time_lookup = defaultdict(int) 
for index, time in enumerate(time1):
	time_lookup[time] = index 

time_block = 0
last_block =0

id_Core = np.zeros((time_lookup[max_time_block],90,90),dtype=np.float64)

with open("fbForum.txt") as outfile: 
	for index, l in enumerate(outfile):
			if (time_block == last_block + 1) or (time_block == last_block): 
				from_id,to_id,time = l.strip().split(" ")

				time_block = int(time)/time_window

			if time_block >= max_time: 	
				print "What",  time_block, index, time_lookup[int(time_block)]
				break

			id_Core[time_lookup[int(time_block)], int(from_id),int(to_id)] += 1 

			if max_time_block < time_block:
				max_time_block = time_block
			last_block  = time_block
			
print max_time_block, "time"

outfile = open('timeVaryingData.npy','w')
np.save(outfile, id_Core)
outfile.close()

out = open('roi_eu_core_ids.txt', 'w')
for index, author in enumerate(range(90)):
	out.write(str(index).encode('utf8')+'\n')
out.close()

out = open('roi_time_manual.txt', 'w')
for index in range(0,max_time_block,1): 
	out.write(str(index).encode('utf8')+'\n')
out.close()


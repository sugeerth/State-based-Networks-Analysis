import json
import numpy as np
from collections import defaultdict
import pprint

import time; 

time_window = 61
offset = 32400

# 203 - 238 
first_off = 78
from_offset = 32400 + first_off*time_window
print from_offset
print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(from_offset))


# print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(32400))
# print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(32400+time_window))

last_off = 178
last_offset = 32400 + last_off*time_window
print last_offset
print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(last_offset))


max_time_block = last_off-first_off + 1 
time1 = set()

from1 = -1
to1 = -1

time_lookup = defaultdict(int) 

for index, time in enumerate(time1):
	time_lookup[time] = index 

counter = 0 
node_lookup = defaultdict(int) 

with open("labels.txt") as outfile: 
	for index, l in enumerate(outfile):
			node, label1, label2 = l.strip().split("\t")
			node_lookup[node] = counter
			counter = counter + 1 
print node_lookup

import pickle
filehandler = open("node_lookup.obj","wb")
pickle.dump(node_lookup,filehandler)
filehandler.close()


outfile.close()
id_Core = np.zeros((max_time_block,242,242),dtype=np.int)

counter = 0
with open("primaryschool.csv") as outfile: 
	for index, l in enumerate(outfile):
			time, from_id,to_id, label1, label2 = l.strip().split("\t")
			time = int(time)
			time = time - 32400
			timeInt = time/time_window

			if (timeInt >= first_off) and (timeInt <= last_off): 
				timeInt = timeInt - first_off
				try: 
					id_Core[timeInt,node_lookup[from_id], node_lookup[to_id]] += 1 
				except IndexError: 
					print "Reached the end folks"
print np.shape(id_Core)

outfile = open('timeVaryingData.npy','w')
np.save(outfile, id_Core)
outfile.close()

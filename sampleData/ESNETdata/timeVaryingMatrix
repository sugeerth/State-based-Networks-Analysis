import json
from pprint import pprint
from collections import defaultdict
import numpy as np
import ast

dataStructure = []

labels = defaultdict()
first = True

# Require Manual intervention 
denomintor = 10000
Offset = 149246000

totalTimeSteps = 39

for i in range(1,8):
	if i == 7: 
		continue
	with open(str(i)+".json") as data_file:    
   		data = json.load(data_file)
   		dataStructure.append(data)
		iteration = data["data"]["mapTopology"]["edges"]
		if first: 
			for i in iteration: 
				name = i['name'].split('--')
				try: 
					labels[str(name[0])] += 1
				except KeyError:
					labels[str(name[0])] = 1
				try: 
					labels[str(name[1])] += 1
				except KeyError:
					labels[str(name[1])] = 1
			first = not(first)

matrix = np.zeros((totalTimeSteps,len(labels),len(labels)))

LookupLabel = dict() 

for index1, key in enumerate(labels.keys()):
	LookupLabel[key] = index1

Max = -999
Min = 999999999999

"""
Now enter the data into the matrix and then give this data to the visualization module
"""
for i in range(1,10):
	if i == 7 or i==9: 
		continue
	# print i, "---File ID"
	with open(str(i)+".json") as data_file:    
   		data = json.load(data_file)
   		dataStructure.append(data)
		iteration = data["data"]["mapTopology"]["edges"]
		for iterationRecord in iteration:
			name = iterationRecord['name'].split('--')
			start = LookupLabel[str(name[0])] 
			end = LookupLabel[str(name[1])]
			record = iterationRecord["traffic"]
			record =json.loads(record)
			# print record["points"],type(record), 
			# print len(record["points"])
			
			# print name[0],name[1]
			
			for t,s,e in record["points"]:
				t= t/denomintor
				t = t-Offset
				t=(t-34)/3

				avg = (s+e)/2
				avg = np.log(avg)
				
				if avg == -np.inf:
					print "hi"

				if matrix[t,start,end] == 0: 
					matrix[t,start,end] = avg
				
				if matrix[t,end,start] == 0: 
					matrix[t,end,start] = avg

				# if s > Max: 
				# 	Max = np.log(s) 

				# if e > Max: 
				# 	Max = np.log(e) 


				# if s < 1000 or e<1000: 
				# 	continue
				# if s < Min: 
				# 	Min = s 

				# if e < Min: 
				# 	Min = e 



np.save("directedMatrix", matrix)

"""
The idea is simple to transform the dataset into a numpy matrix with the data and then have an order of the indices. 
"""



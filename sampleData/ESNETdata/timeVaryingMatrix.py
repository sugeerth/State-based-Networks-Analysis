import json
from pprint import pprint
from collections import defaultdict
import numpy as np
import ast
import json

dataStructure = []

labels = defaultdict()
first = True

# Require Manual intervention 
denomintor = 100000
Offset = 14980788

#289
totalTimeSteps = 300
# 1495092000000
stopTime = Offset * denomintor + (totalTimeSteps * 18 * denomintor)
print stopTime

with open("24HrEpoch.json") as data_file:    
	d = json.load(data_file)
	for i,j in enumerate(d):
		c = d[i]["name"]
		labels[c] = 0


labels["esnet-east"] = 0 
labels["esnet-west"] = 0 
labels["nersc"] = 0 

print labels

LookupLabel = dict() 

for index1, key in enumerate(labels.keys()):
	key = key.upper()
	LookupLabel[str(key)] = index1

print LookupLabel

timeVaryingMatrix = np.zeros((totalTimeSteps,len(labels),len(labels)))

"""
Parsing the dataset and then what is it doing storing the connectvitiey 
datasets into a matrix for transformiation
"""
with open('24HrEpoch.json') as json_data:
	d = json.load(json_data)

	labels = [] 
	for i,j in enumerate(d):
		start = d[i]["name"]
		labels.append(start)
		try: 
			start = int(LookupLabel[str(start.upper())]) 
		except KeyError: 
			print "KEY1"
			continue
		
		for k, flow in enumerate(d[i]["data"]["networkEntity"]["flow"]):
			c = json.loads(d[i]["data"]["networkEntity"]["flow"][k]["traffic"])

			for t,s,e in c["points"]:
				if t == stopTime:
					break
				try: 
					end = int(LookupLabel[str(c["name"].upper())]) 
				except KeyError: 
					print "NOT FOUND",c["name"].upper()
					continue
				
				t= t/denomintor
				t= t-Offset
				t= t/18

				avg1 = (s+e)/2
				
				try: 
					avg = np.log(avg1)
				except RuntimeError:
					print "HI"
				
				if avg == -np.inf:
					continue

				if timeVaryingMatrix[t,start,end] == 0: 
					timeVaryingMatrix[t,start,end] = avg


print timeVaryingMatrix, len(labels)
np.save("timeVaryingData", timeVaryingMatrix)
np.save("labelsChange", labels)

"""
The idea is simple to transform the dataset into a numpy matrix with the data and then have an order of the indices. 
"""





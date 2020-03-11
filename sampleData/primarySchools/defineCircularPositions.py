import os
import os.path as path
import pickle
import networkx as nx
import csv

brainDataNetwork = None
brainDataObject = None

PrimarySchoolslabelFilename = "labels.txt" 
data = {1:2,
2:3,
3:4,
4:5,
5:1} 
from collections import defaultdict
dicti = defaultdict(list)
counter0 = 1
def defineCircularLayout(className,nodes, minx1,minx2, middle = False):
	global counter0, dicti
	dicti[int(className)] = nodes

	counter0 += 1

	G=nx.path_graph(len(nodes))

	if not(middle):
		pos=nx.circular_layout(G,  scale=1)
	else: 
		pos=nx.circular_layout(G,  scale=0.65)

	max1 = -999
	max2 = -999
	min1 = 999
	min2 = 999
	for id, val in pos.items():
		if min1 > val[0]:
			min1 = val[0]
		if min2 > val[1]:
			min2 = val[1] 
		if max1 < val[0]:
			max1 = val[0]  
		if max2 < val[1]:
			max2 = val[1] 

		val[0] = minx1 + val[0]
		val[1] = minx2 + val[1]

	print min1,min2,max1,max2
	return pos

class mainModel(object):
    def __init__(self):
		file = open("node_lookup.obj",'rb')
		self.node_lookup = pickle.load(file)
		file.close()
		counter = 0 
		node_lookup = [] 
		from collections import defaultdict
		self.communityPos = defaultdict(list)

		with open(PrimarySchoolslabelFilename, 'r') as outfile: 
			for index, l in enumerate(outfile):
				node, label1, label2 = l.strip().split("\t")
				self.communityPos[label1[0]].append(self.node_lookup[node])
				node_lookup.append(label1)

		positions = dict()
		offset = [0,0] 
		self.communityCircPos = defaultdict(list)

		for className, nodes in self.communityPos.items():
			print className
			if className == "1": 
				self.communityCircPos[int(className)] = defineCircularLayout(className,nodes, 4.15, 2.25)
			elif className == "2":
				self.communityCircPos[int(className)] = defineCircularLayout(className,nodes, 0.45, 0)
			elif className == "3": 
				self.communityCircPos[int(className)] = defineCircularLayout(className,nodes, 4.95, 0)
			elif className == "4": 
				self.communityCircPos[int(className)] = defineCircularLayout(className,nodes, 2.75, -1.50)
			elif className == "5": 
				self.communityCircPos[int(className)] = defineCircularLayout(className,nodes, 1.45, 2.25)


		ofile  = open('positions.csv', "wb")
		writer = csv.writer(ofile, delimiter=',')
		
		import pprint
		pprint.pprint(self.communityCircPos) 
		for i, value in self.communityCircPos.items():
			counter = len(dicti[i]) -1
			for id, pos in value.items():
				print id, "value", i, counter, len(dicti[i]),dicti[i][counter], i
				writer.writerow((dicti[i][counter],"{0:.4f}".format(pos[0]),"{0:.2f}".format(pos[1])))
				counter =counter - 1
		ofile.close()

def main():
	selfi = mainModel()


#start process
if __name__ == '__main__':
    main()
import numpy as np
import networkx as nx
# import bct
import community as cm 
import pprint
import copy
import math
from colorBrewer import *
from collections import defaultdict
from operator import itemgetter
from collections import OrderedDict
from collections import OrderedDict
from collections import Counter


"""
This is the data that needs to be changed based on the format of the data
"""

class modelAverageGraphs(object):
	def __init__(self, dataProcessingBrainObject):
		self.dataProcessingBrainObject = dataProcessingBrainObject
		self.distanceMatrix = self.dataProcessingBrainObject.distanceMatrix

	def returnModelledAverageGraphsObject(self, states):
		"""
		So here for each interval 1: (x,y) there exist a graph structure that is representative of 
		state dynamics for that particular visualization

		We can think of this as a class that models the entire hierarchy structure in 
		the hierarcical timeNode Data Strcuture
		"""
		self.distanceMatrix = self.dataProcessingBrainObject.distanceMatrix
		intervalList = [] 
		for j in range(self.dataProcessingBrainObject.levels):
			# print j,"th LEVEL IN MODELLING"
			for i, childNode in enumerate(self.dataProcessingBrainObject.NodeLevels[j]):
				dataFound = False
				# print childNode.level, childNode.interval, childNode.reducedNetworkxGraph, "IN MODELLING"
				for index, data in enumerate(intervalList):
					if data == (childNode.interval[0],childNode.interval[1]):  
						# print "FOOUND THE CULPRIT", data, j,"th LEVEL","IN MODELLING"
						childNode.reducedNetworkxGraph = nx.from_numpy_matrix(finalMatrix)
						childNode.reducedCommunityAssignments = communityColorDict
						childNode.reducedMatrix = np.array(finalMatrix)
						intervalList.append((childNode.interval[0],childNode.interval[1]))
						dataFound = True
						break
				if dataFound: 
					continue

				if childNode.interval[0] > childNode.interval[1]:
					a = int(childNode.interval[1]) 
					b = int(childNode.interval[0])
				else: 
					a = int(childNode.interval[0]) 
					b = int(childNode.interval[1])

				intervalMatrix = self.distanceMatrix[a:b,a:b]
				
				intervalList.append((a,b))

				columns = (intervalMatrix != 0).sum(0)
				rows    = (intervalMatrix != 0).sum(1)

				columnsAvg = (intervalMatrix != 0).mean(0)
				rowsAvg    = (intervalMatrix != 0).mean(1)

				# print len(rows), "ROWS"
				topKValues = int(math.ceil(0.26*len(rows)))
				# print topKValues, "Values"
				topTimeSteps = rowsAvg.argsort()[-topKValues:][::-1]
				topTimeSteps = childNode.interval[0]+topTimeSteps

				communityColorDict = dict()
				allCommunityColors = dict()

				allNodes = self.dataProcessingBrainObject.timeSeriesData[0]["nodes"]
				length = len(allNodes)

				firstSwap = True

				if firstSwap:
					storageMatrix = np.zeros((topKValues,length,length))
					varianceMatrix = np.zeros((length,length))
					standardDeviationMatrix = np.zeros((length,length))

				for l in allNodes: 
					nodeID = l["node"]
					colorDict = {}
					additionMatrix = np.zeros((length,length))
					maskMatrix = np.full((length,length), True, dtype=bool)
					prunedEdgesMatrix = np.full((length,length), True, dtype=bool)
					counter = 0
					lastone = 0
					for k in topTimeSteps:
						"Finding Average communities, edges, and edge weights"
						color = self.dataProcessingBrainObject.timeSeriesData[k]["nodes"][nodeID]["color"]
						try: 
							colorDict[color] += 1 
						except KeyError:
							colorDict[color] = 1

						if firstSwap:
							graphG = self.dataProcessingBrainObject.graphDataStructureList[k]
							x1 = self.dataProcessingBrainObject.timestepNetworkData[k]
							masked = x1 > 0
							maskMatrix = np.logical_and(maskMatrix, masked)
							# print lastone, np.sum(maskMatrix),abs(lastone-np.sum(maskMatrix)), "Hello there", topTimeSteps
							lastone = np.sum(maskMatrix)
							additionMatrix = np.add(additionMatrix, x1) 
							storageMatrix[counter] = x1
							counter = counter + 1
					
					d = Counter(colorDict)
					value = d.most_common()[0]
					communityColorDict[nodeID] = value[0]
					allCommunityColors[nodeID] = d

					if firstSwap: 
						maskMatrix = 1*maskMatrix
						additionMatrix = additionMatrix/topKValues
						finalMatrix = np.multiply(maskMatrix,additionMatrix)
						standardDeviationMatrix = np.multiply(maskMatrix,np.ndarray.std(storageMatrix, axis=0))
						varianceMatrix = np.multiply(maskMatrix,np.ndarray.var(storageMatrix, axis=0))
						firstSwap = False

				childNode.reducedNetworkxGraph = nx.from_numpy_matrix(finalMatrix)
				childNode.topTimeSteps = topTimeSteps
				childNode.reducedCommunityAssignments = communityColorDict
				# print allCommunityColors
				childNode.distributionOfCommunityAssignments = allCommunityColors
				childNode.storageMatrix = storageMatrix
				childNode.reducedMatrix = np.array(finalMatrix)
				childNode.reducedStandardDeviationMatrix = np.array(standardDeviationMatrix)
				childNode.reducedVarianceMatrix = np.array(varianceMatrix)

		return self.dataProcessingBrainObject.stateHierarchy



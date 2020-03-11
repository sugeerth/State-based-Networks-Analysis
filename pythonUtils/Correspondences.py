import numpy as np
import networkx as nx
# import bct
import community as cm 
import pprint
import copy
import math
from colorBrewer import *
from collections import defaultdict
from TemporalMetric import TemporalMetric
from GraphAlgorithms.DistanceMetrics import DistanceForBrainRegions,CSRMax, RootSim

"""
This is the data that needs to be changed based on the format of the data
"""

THRESHOLDVALUE = 0.40

T_C = 0.9
DELTA = 0.1 

LocalHaloThreshold = 0.07
GlobalChangeThreshold = 0.07

import numpy as np
import colorsys

def _get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors

class Correspondence(object):
	def __init__(self, dataProcessingBrainObject):
		self.colorPalletes = qualitative['Set3']
		self.dataProcessingBrainObject= dataProcessingBrainObject
		self.similarityMatrix = np.zeros((204,dataProcessingBrainObject.length,dataProcessingBrainObject.length))
		self.similarityMatrixTV = np.zeros((204,204,dataProcessingBrainObject.length,dataProcessingBrainObject.length))

		self.colorsThresholdValue = 0.20
		self.dataProcessingBrainObject = dataProcessingBrainObject
		self.temporalMetric = TemporalMetric(self)
		
		self.globalSimilarityMetric = dict()
		self.edgePersistanceIndividual = dict()

		self.overallMetric = dict()

		self.edgePersistanceMetric = dict()
		self.topologicalChangesMetric = dict()

		self.Dataset1 = None
		self.Dataset2 = None

		self.timeStep = 0

		self.avg = 0

		self.colorsD = qualitative['Set3'][12] 

		self.assignmentCounter = 0
		self.colorCounter = 0

	"""
	determine the new value of the Dataset1 and return the values
	The data model of the visualization is
	Dataset1 is current and Dataset2 is previous
	TimeData == "Nodes", "Links", "Groups", "Modularity"
	"""
	def findCorrespondence(self, Dataset1, Dataset2, timeStep):
		nodeDict1 = Dataset2['nodes'] # nodedict1 is previous
		nodeDict2 = Dataset1['nodes'] # nodedict2 is current

		# print timeStep, "TimeStep"
		self.timeStep = timeStep
		self.Dataset1 = Dataset1
		self.Dataset2 = Dataset2

		community1 = np.zeros(len(nodeDict1))
		community2 = np.zeros(len(nodeDict2))

		currentDataStructure, previousDataStructure = self.wrapToCommunitiesDataStructure(nodeDict1,nodeDict2) 
		self.similarityMatrix[timeStep], realMatrix = self.findSimilarityMatrix(currentDataStructure,previousDataStructure)
		self.assignColorsBetweenNodes(nodeDict1,nodeDict2,currentDataStructure, previousDataStructure,realMatrix)

	def findSimilarityValues(self, Dataset1, Dataset2, timeStep1, timeStep2):
		
		nodeDict1 = Dataset2['nodes'] # nodedict1 is previous
		nodeDict2 = Dataset1['nodes'] # nodedict2 is current

		community1 = np.zeros(len(nodeDict1))
		community2 = np.zeros(len(nodeDict2))

		currentDataStructure, previousDataStructure = self.wrapToCommunitiesDataStructure(nodeDict1,nodeDict2) 
		ignoreValue, realMatrix = self.findSimilarityMatrix(currentDataStructure,previousDataStructure)
		similarity = self.pairwiseAverageSim(nodeDict1, nodeDict2, currentDataStructure, previousDataStructure, realMatrix, timeStep1, timeStep2)

		return similarity

	def wrapToCommunitiesDataStructure(self,nodeDict1, nodeDict2):
		currentDataStructure = defaultdict(list)
		previousDataStructure = defaultdict(list)

		for i,j in zip(nodeDict1,nodeDict2):
			currentDataStructure[i["group"]].append((i["node"],i["color"]))
			previousDataStructure[j["group"]].append(j["node"])

		return currentDataStructure, previousDataStructure

	def findSimilarityMatrix(self, current, previous):
		Kappa_matrix = np.zeros((self.dataProcessingBrainObject.length, self.dataProcessingBrainObject.length))

		realMatrix = np.zeros((len(current),len(previous)))
		counter1 = 0 
		counter2 = 0 
		for community1, nodes1 in current.items():
			counter2 = 0  
			nodes1 = [i for i,j in nodes1]
			nodes1 = tuple(nodes1)
			for community2, nodes2 in previous.items():
				elements = len(list(set(nodes1).intersection(nodes2)))
				Numerator = elements
				Denominator = len(list(set(nodes1).union(nodes2)))
				val = float(float(Numerator)/float(Denominator))
				Kappa_matrix[counter1][counter2] = val
				realMatrix[counter1][counter2] = val
				counter2 = counter2 + 1 
			counter1 = counter1 + 1 

		return Kappa_matrix, realMatrix

	def assignColorsBetweenNodes(self, node1, node2,current, previous, similarity):
		Assignment = defaultdict(list)

		KappaMatrixForComputation = []
		x, y = similarity.shape

		KappaMatrixForComputation = copy.deepcopy(similarity)
		ColorAssignment = dict()
		similaritySum = 0
		counter = 0

		if x >= 1 and y >= 1: 
			height = len(KappaMatrixForComputation[:,0])
			width = len(KappaMatrixForComputation[0])

			"""
			Naive algorithm to assign stuff
			"""
			while True:
				if (len(ColorAssignment.keys()) == width) or (len(ColorAssignment.values()) == height) or KappaMatrixForComputation.any() == 0:
					break 
				m,n = np.unravel_index(KappaMatrixForComputation.argmax(), KappaMatrixForComputation.shape)
				ColorAssignment[n] = m
				counter+=1
				similaritySum += KappaMatrixForComputation[m,n]
				KappaMatrixForComputation[m] = 0
				KappaMatrixForComputation[:,n] = 0 
				KappaMatrixForComputation[m,n] = 0

			"""adding new colors"""
			AssignedValues = []
			# for m,color in ColorAssignment.values(): 
				# AssignedValues.append(m)
			# AssignedValues = set(AssignedValues)

			# AssignedKeys = set(AssignedKeys)
			AssignedValues = set(ColorAssignment.values())
			AssignedKeys = set(ColorAssignment.keys())

			allElementsHeight = set(range(0,height))
			DifferenceElements = allElementsHeight - AssignedValues

			"""Case when some community colors are born again"""

			allElements = set(range(0,width))
			NewBornCommunities = allElements-AssignedKeys
			
			# The average indicates how much is common among the two network structures
			self.avg = float(similaritySum/counter)

			# print ColorAssignment, NewBornCommunities 
			# if NewBornCommunities:
			# 	NewBornCommunities = list(NewBornCommunities)
				# print NewBornCommunities[0], previous[NewBornCommunities[0]]

			self.assignmentCounter+=1
			for q in NewBornCommunities:
				colors = self.colorsD[self.colorCounter]
				colors=colors.strip()
				colors=colors.replace("rgb(", "rgba(")
				colors=colors.replace(")", ","+str(1)+")")
				ColorAssignment[q] = colors
				self.colorCounter = (self.colorCounter + 1 )% 19

		self.assignColors(ColorAssignment, node1, node2, current, previous, similarity)
		return ColorAssignment

	def assignColors(self,ColorAssignment, nodeDict1, nodeDict2, current, previous,similarity):
		allNodes = [i for i in range(self.dataProcessingBrainObject.nodeLength)]

		for toCommunity,fromCommunity in ColorAssignment.items():
			# checking if the algorithm already assigned a color?
			if not(isinstance(fromCommunity,str)):
				try: 
					colorsToMap = current[fromCommunity][0][1]
				except IndexError:
					colors = self.colorsD[self.colorCounter]
					colorsToMap = colors
					self.colorCounter = (self.colorCounter + 1) % 19

				currentData = [i for i,j in current[fromCommunity]]
				comparisonData = (current[fromCommunity], previous[toCommunity])
				
				for i in previous[toCommunity]: # this is the data from the previous nodes you are getting the colors 
					NodeKey = self.Dataset1["nodes"][i]
					allNodes.remove(NodeKey['node'])
					NodeKey['color'] = colorsToMap
			else:
				for i in previous[toCommunity]:
					NodeKey = self.Dataset1["nodes"][i]
					allNodes.remove(NodeKey['node'])
					NodeKey['color'] = fromCommunity
		counter = 0
		if allNodes:
			for i in allNodes:
				counter+=1
				NodeKey = self.Dataset1["nodes"][i]
				# print NodeKey
				# NodeKey['color'] = self.colorsD[self.colorCounter]
				# self.colorCounter = (self.colorCounter + 1 )% 20
				# print "Actual node Id", i,NodeKey['group'], "Its color",NodeKey['color'],current[NodeKey['group']]
				# self.colorCounter = (self.colorCounter + 1 )% 20
		
		colors = []
		for k in self.Dataset1["nodes"]:
			colors.append(k['color'])

		maxTopologicalOverlap = -999 
		minTopologicalOverlap = 999

		maxGlobalOverlap = -999 
		minGlobalOverlap = 999

		similarity,diffsimilarity,deltaSimilarityValueLocal,minTopologicalOverlap,maxTopologicalOverlap,minGlobalOverlap, maxGlobalOverlap  = self.averageSimilarity(nodeDict1, nodeDict2, current, previous, similarity, maxTopologicalOverlap, minTopologicalOverlap, maxGlobalOverlap, minGlobalOverlap)
		self.Dataset1['colors'] = colors

		# FIXME 
		self.Dataset1['avgSimilarity'] = similarity
		self.Dataset1['1-avgSimilarity'] = (1- similarity)
		self.Dataset1['diffSimilarity'] = abs(diffsimilarity)

		if maxTopologicalOverlap > self.dataProcessingBrainObject.GlobalmaxTopologicalOverlap: 
			self.dataProcessingBrainObject.GlobalmaxTopologicalOverlap = maxTopologicalOverlap

		if minTopologicalOverlap < self.dataProcessingBrainObject.GlobalminTopologicalOverlap:
			self.dataProcessingBrainObject.GlobalminTopologicalOverlap = minTopologicalOverlap 

		if  maxGlobalOverlap > self.dataProcessingBrainObject.GlobalmaxGlobalOverlap: 
			self.dataProcessingBrainObject.GlobalmaxGlobalOverlap = maxGlobalOverlap

		if minGlobalOverlap < self.dataProcessingBrainObject.GlobalminGlobalOverlap:
			self.dataProcessingBrainObject.GlobalminGlobalOverlap = minGlobalOverlap 

		self.Dataset1['maxTopologicalOverlap'] = maxTopologicalOverlap
		self.Dataset1['minTopologicalOverlap'] = minTopologicalOverlap
		self.Dataset1['onlyOneValue'] = ("false","true")[minTopologicalOverlap == maxTopologicalOverlap]
		
#		self.Dataset1['LocalTopologicalOverlap']  = deltaSimilarityValueLocal

		self.Dataset1['maxGlobalOverlap'] = maxGlobalOverlap
		self.Dataset1['minGlobalOverlap'] = minGlobalOverlap
		self.Dataset1['onlyOneValueGlobal'] = ("false","true")[maxGlobalOverlap == minGlobalOverlap]

		# finding the average of non-zero elements in the similarity matrix
		# Sum = np.sum(similarity)
		# count = np.count_nonzero(similarity)
		# avg = float(Sum/count)
		# self.Dataset1['avgSimilarity'] = avg

	def pairwiseAverageSim(self, nodeDict1, nodeDict2, current, previous,similarity, i, j):
		"""
		Defined for computing the matrix
		Defines the pairwise similarity sum of all the data present in the dataset
		"""
		# KappaMatrixForComputation = []
		# ColorAssignment = dict()
		# x, y = similarity.shape

		# KappaMatrixForComputation = copy.deepcopy(similarity)
		# similaritySum = 0
		# counter = 0

		# if x >= 1 and y >= 1: 
		# 	height = len(KappaMatrixForComputation[:,0])
		# 	width = len(KappaMatrixForComputation[0])

		# 	"""
		# 	Naive algorithm to assign stuff
		# 	"""
		# 	while True:
		# 		if (len(ColorAssignment.keys()) == width) or (len(ColorAssignment.values()) == height) or KappaMatrixForComputation.any() == 0:
		# 			break 
		# 		m,n = np.unravel_index(KappaMatrixForComputation.argmax(), KappaMatrixForComputation.shape)
		# 		ColorAssignment[n] = m
		# 		counter+=1
		# 		similaritySum += KappaMatrixForComputation[m,n]
		# 		KappaMatrixForComputation[m] = 0
		# 		KappaMatrixForComputation[:,n] = 0 
		# 		KappaMatrixForComputation[m,n] = 0

		# 	# The average indicates how much is common among the two network structures
		# 	localAvg = float(similaritySum/counter)

		# similarity = np.zeros(self.dataProcessingBrainObject.length)

		# for i in range(self.dataProcessingBrainObject.length):
		# 	similarity[i] = self.defineChanges(i,self.dataProcessingBrainObject.timestepNetworkData[i],self.dataProcessingBrainObject.timestepNetworkData[j],self.dataProcessingBrainObject.length)

		# similarity = T_C*localAvg+DELTA*np.mean(similarity)

		similarity = self.deltaCon(i,self.dataProcessingBrainObject.timestepNetworkData[i],self.dataProcessingBrainObject.timestepNetworkData[j],self.dataProcessingBrainObject.length)

		return similarity


	def averageSimilarity(self, nodeDict1, nodeDict2, current, previous,similarity, maxTopologicalOverlap, minTopologicalOverlap,maxGlobalOverlap, minGlobalOverlap):
		"""
		Defines the average similarity according ot the manuscript
		"""
		self.globalSimilarityMetric[self.timeStep] = self.avg

		LocalSimilarity = np.zeros(self.dataProcessingBrainObject.length)
		# deltaSimilarityValueLocal = np.zeros(self.dataProcessingBrainObject.length)
		deltaSimilarityValueLocal = dict()

		# Computing the similairty metric here, What really happens here is the question 
		for i in range(self.dataProcessingBrainObject.length):
			LocalSimilarity[i] = self.defineChanges(i,self.dataProcessingBrainObject.timestepNetworkData[self.timeStep-1],self.dataProcessingBrainObject.timestepNetworkData[self.timeStep],self.dataProcessingBrainObject.length)

		self.edgePersistanceIndividual[self.timeStep] = LocalSimilarity
		# similarity = T_C*self.avg+DELTA*np.mean(similarity)
		similarity = self.deltaCon(i,self.dataProcessingBrainObject.timestepNetworkData[self.timeStep-1],self.dataProcessingBrainObject.timestepNetworkData[self.timeStep],self.dataProcessingBrainObject.length)
		self.edgePersistanceMetric[self.timeStep] = similarity

		#FIX ME 
		deltaSimilarityValueGlobal = 0
		if self.timeStep >1:
			value = self.changedifference(self.edgePersistanceMetric[self.timeStep-1], self.edgePersistanceMetric[self.timeStep])
			if abs(value) > GlobalChangeThreshold: 
				if value > maxGlobalOverlap: 
					maxGlobalOverlap = value
				if value < minGlobalOverlap:
					minGlobalOverlap = value
				deltaSimilarityValueGlobal = value

			for i in range(self.dataProcessingBrainObject.length):
				value = self.changedifference(self.edgePersistanceIndividual[self.timeStep-1][i], self.edgePersistanceIndividual[self.timeStep][i])
				if abs(value) > LocalHaloThreshold: 
					if value > maxTopologicalOverlap: 
						maxTopologicalOverlap = value
					if value < minTopologicalOverlap:
						minTopologicalOverlap = value
					deltaSimilarityValueLocal[i] = value
		else: 
			deltaSimilarityValueGlobal = 0

		self.overallMetric[self.timeStep] = similarity
		return similarity, deltaSimilarityValueGlobal, deltaSimilarityValueLocal,minTopologicalOverlap, maxTopologicalOverlap,minGlobalOverlap,maxGlobalOverlap

	def changedifference(self, similarityPrev, similarityCurrent):
		absValue = similarityCurrent-similarityPrev
		if absValue ==0: 
			return 0
		if absValue == float('Inf') or math.isnan(float(absValue)):
			absValue = 0
		return absValue

	def changeWeightedComparison(self, similarityPrev, similarityCurrent):
		try: 
			absValue = abs(similarityCurrent-similarityPrev)
			if absValue ==0: 
				return 0
			metric = absValue/similarityPrev
		except ZeroDivisionError:
			metric = 0
		if metric == float('Inf') or math.isnan(float(metric)):
			metric = 0
		return metric

	def defineChanges(self, seedNode, previousMatrix, currentMatrix, length):
		sumSeedNode = 0
		sumK = 0 
		sumL = 0
		for i in range(length-1):
			k = previousMatrix[seedNode,i]
			l = currentMatrix[seedNode,i]
			sumK+=k
			sumL+=l
			if not(k==0) and not(l==0): 
				sumSeedNode += k*l
		product = sumK*sumL
		sq = math.sqrt(product)

		if sumSeedNode == 0: 
			return 0

		if sq == 0: 
			return 0 

		try: 
			fraction = sumSeedNode/sq
		except ZeroDivisionError:
			fraction = 0
		return fraction

	"""
		DELTACON implementation of the similarity matrix
		Please finish it by 4:00 pm
	"""
	def deltaCon(self, i, previous, next,length): 
		previousData = nx.from_numpy_matrix(previous)
		nextData = nx.from_numpy_matrix(next)

		previousDData = DistanceForBrainRegions(previousData)
		nextDData = DistanceForBrainRegions(nextData)

		PCSRMax = CSRMax(previousDData,length)
		NCSRMax = CSRMax(nextDData,length)

		Pdelta = 1/(1+PCSRMax)
		Ndelta = 1/(1+NCSRMax)

		I = np.identity(length, dtype=None)
		FinalMatrix = np.zeros((length,length))

		Pdelta2 = Pdelta**2
		IntermediateMatrix = I + Pdelta2* previousDData - Pdelta*previous
		PFinalMatrix = np.linalg.inv(IntermediateMatrix)

		Ndelta2 = Ndelta**2
		IntermediateMatrix = I + Ndelta2* nextDData - Ndelta*next
		NFinalMatrix = np.linalg.inv(IntermediateMatrix)

		sim = 0
		d = RootSim(PFinalMatrix, NFinalMatrix)
		sim = 1/(1+d)
		# print sim

		return sim

	def determineTopologicalCorrespondence(self, Dataset1,Dataset2):
		"""
		This is a bit tricky because you would need to go over all the resolutions 
		parameters of the clustering result and look at the clustering resutl

		TimeData == "Nodes", "Links", "Groups", "Modularity"
		For Each node there is a corresponding Level value to it 
		"""
		pass

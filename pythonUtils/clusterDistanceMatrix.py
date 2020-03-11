import numpy as np
import networkx as nx
import community as cm 
from colorBrewer import *
import pprint
from collections import defaultdict
import numpy as np
from hierarchicalTimeNodeDataStructure import Node
from scipy.signal import argrelextrema
from collections import Counter
import pickle


# threshold in the for visualization in the tool
DISTANCE_MATRIX_VISUALIZATION_METRIC = 0.00

# threshold in the similarity to be used for analysis of the data 
REAL_MATRIX_THRESHOLD = 0.00

class clusterDistanceMatrix(object):
    def __init__(self, baseObject):
        self.dataProcessingObject = baseObject
        self.timestepPartition = None
        self.first = False

    def deriveHierarchicalStructure(self, states):
        """
        Please NOTE that this is pretty much data driven and I have hardcorded teh values for 3 levels
        This can definelty be xtended to numerous levels
        """
        self.dataProcessingObject.levels = len(states)

        root = Node(0, 0,-1)
        # highest levels of the node 
        # self.NodeLevels 
        
        for i in xrange(self.dataProcessingObject.levels):
            ll = []
            for stateNo, intervals in states[i].items():
                if intervals[0]==intervals[1]: 
                    continue
                if i == 0: 
                    child = Node(intervals[0],intervals[1], i)
                    root.add_child(child)
                    ll.append(child)
                elif i == 1: 
                    child = Node(intervals[0],intervals[1], i)
                    childNode = root.lookupNodetoBeAdded((intervals[0],intervals[1], i))
                    childNode.add_child(child)
                    ll.append(child)
                else:
                    child = Node(intervals[0],intervals[1], i)
                    childNode = root.lookupNodetoBeAdded((intervals[0],intervals[1]))
                    childChildNode = childNode.lookupNodetoBeAdded((intervals[0],intervals[1]))
                    childChildNode.add_child(child)  
                    ll.append(child)
            self.dataProcessingObject.NodeLevels[i] = ll
        return root

    def clusterDistanceMatrix(self, distanceMatrix = []):
        """
        Gets the similarity distance matrix to identify the topological structure that is most similar
        over different time-frames.         
        """
        # pprint.pprint(distanceMatrix) 
        # graph = nx.from_numpy_matrix(distanceMatrix)
        # partition = cm.best_partition(graph)

        # communityMultiple = defaultdict(list)

        # for node, group in partition.items():
        #     communityMultiple[group].append(node)

        # # Now based on the partition we can detect the nodes in to different 
        # # states that will best represent the underlying data
        # states1 = dict()
        # states2 = dict()

        # lastEnd = 0
        # """
        # Identifying graphs and standards and changes
        # """
        # for index, nodes in communityMultiple.items():  
        #     start = nodes[0]
        #     end = nodes[-1]
        #     # Things to do for the temporal contunuity of data
        #     if (lastEnd > start):
        #         if (lastnodes[-2] > start):
        #             states1[index-1][1] = start-1
        #         else: 
        #             states1[index-1][1] = lastnodes[-2]
        #     states1[index] = [start, end]
        #     lastEnd = end
        #     lastnodes = nodes

        # index2 = 0
        # """
        # Identifying graphs and standards and changes
        # """
        # for index, interval in states1.items():
        #     numpyMatrix = self.dataProcessingObject.distanceMatrix[interval[0]:interval[1],interval[0]:interval[1]]
        #     graph = nx.from_numpy_matrix(numpyMatrix)
            
        #     partition2 = cm.best_partition(graph)
        #     communityMultiple2 = defaultdict(list)

        #     for node, group in partition2.items():
        #         communityMultiple2[group].append(interval[0]+node)

        #     lastIndex = index2
        #     lastEnd1=0
        #     lastnodes1 = []
        #     for i, values in communityMultiple2.items():
        #         if len(values) == 1:
        #             index2 = lastIndex + i
        #             states2[index2] = [values[0],values[0]] 
        #             continue;
        #         start1 = values[0]
        #         end1= values[-1]
        #         index2 = lastIndex + i
        #         # Things to do for the temporal contunuity of data
        #         if (lastEnd1 > start1):
        #             if (lastnodes1[-2] > start1):
        #                 states2[index2-1][1] = start1-1
        #             else: 
        #                 states2[index2-1][1] = lastnodes1[-2]
        #         states2[index2] = [start1, end1]
        #         lastEnd1 = end1
        #         lastnodes1 = values
        #     lastIndex = index2

        states = dict()
        # states12 = {0: [0, 16], 1: [13, 15], 2: [16, 28]}
        # states12 = {0: [0, 20], 1: [21, 54], 2: [56, 78]}

        states12 = {0: [11, 13], 1: [35, 38], 2: [47, 48],3: [49, 52]}

        states13 = {0: [0, 7], 1: [6, 35], 2: [36, 52], 3: [53, 78]}
        states[0] = states12
        # states[1] = states13

        return states

    def defineDistanceMatrixForVisualization(self, timesteps, timeSeriesData, SimilarityObject, TimeWindow, distanceMatrix):
        """
        Distance metrics that can be used to identify the states for a given network datasets
        """
        # import pickle
        # # Saving the objects:
        # with open('pickleDumps/objs.pkl', 'w') as f:  # Python 3: open(..., 'wb')
        #     pickle.dump([timesteps, timeSeriesData, SimilarityObject, distanceMatrix], f)

        half = TimeWindow/2

        for i in range(timesteps):
            if i < half: 
                start = 0 
                end = i+TimeWindow
            elif i>half and (i<(timesteps-half)): 
                start = i-half
                end = i+half
            else: 
                start = i-TimeWindow
                end = timesteps
            if start < 0: 
                start = 0 
            if end > timesteps: 
                end = timesteps
                
            for j in range(start,end,1):
                if i == j: 
                    distanceMatrix[i][j] = 1
                elif i<j:
                    sim = SimilarityObject.findSimilarityValues(timeSeriesData[i],timeSeriesData[j],i,j)
                    distanceMatrix[i][j] = self.thresholdBoolean(REAL_MATRIX_THRESHOLD, sim)

        # with open('pickleDumps/distanceMatrix.pkl') as f:  # Python 3: open(..., 'rb')
        #      distanceMatrix = pickle.load(f)

        return distanceMatrix

    def writeSimilarityValuesForVisualization(self, distanceValues):
        """
        Write the similarity values inside the matrix for matrix evaluation
        """
        for i, value in enumerate(self.dataProcessingObject.timeSeriesData):
            valueDict = dict()
            for j, value1 in enumerate(distanceValues[i]):
                valueDict[j] = self.thresholdBoolean(DISTANCE_MATRIX_VISUALIZATION_METRIC, value1)

            value["distanceValues"] = valueDict

            self.dataProcessingObject.timeSeriesData[i] = []
            self.dataProcessingObject.timeSeriesData[i] = value

    def thresholdBoolean(self, threshold, value):
        """
        Threshold data values so you can better understand the datasets
        """
        return 0 if (threshold > value) else value

    def identifyLocalMaxima(self): 
        """
        Find out the peaks in the data and then identify the timepoints where the similarity can be computed
        """
        x = np.array(self.corres.overallMetric.values())
        extrema = argrelextrema(x, np.greater)
        extremaDicts = dict()

        for i in np.nditer(extrema):
            if self.corres.overallMetric[i+1] < 0: 
                continue
            extremaDicts[i+1] = self.corres.overallMetric[i+1]

        self.threshold1 = np.mean(extremaDicts.values())+2*np.std(extremaDicts.values())
        self.threshold2 = np.mean(extremaDicts.values())+np.std(extremaDicts.values())
        self.threshold3 = np.mean(extremaDicts.values())+0.2*np.std(extremaDicts.values())

        states1 = self.identifyStates(extremaDicts, self.threshold1)
        states2 = self.identifyStates(extremaDicts, self.threshold2)
        states3 = self.identifyStates(extremaDicts, self.threshold3)

        states = dict()
        states[0] = states1
        states[1] = states2
        states[2] = states3

        return states

    def identifyStates(self, extremaDicts, threshold): 
        from operator import itemgetter
        sortedDict = sorted(extremaDicts.items(), key=itemgetter(1)) 

        states = []
        # Prunning based on a threshold value
        # for local minima
        for i,j in sortedDict:
            if j >= threshold:
                states.append(i)

        sortedStates = sorted(states)
        stateDict = dict()
        start = 0
        i = 0  

        for value in sortedStates:
            stateDict[i] = [start, value-1]
            start = value + 1 
            i = i + 1 
        
        stateDict[i] = [value+1, len(self.corres.overallMetric)]

        """
        Values computing the statistics of the various states
        """

        timestepCorrelationValue = np.zeros((len(self.corres.edgePersistanceIndividual[1]),len(self.corres.edgePersistanceIndividual)+1))

        for timestep, similarityArray in self.corres.edgePersistanceIndividual.items(): 
            for i,value in enumerate(similarityArray): 
                timestepCorrelationValue[i][timestep] = float(value)

        for start, end in stateDict.items(): 
            column = timestepCorrelationValue[:, end[0]:end[1]]            
            densityColumn = self.densityList[end[0]:end[1]]
            modularityColumn = self.modularityList[end[0]:end[1]]

            x = column.mean(axis=1)

            print "Temporal Correlation:"
            print x.mean()

            print "Modularity:"
            print modularityColumn.mean(),

            print "Density:"
            print densityColumn.mean()

        print "DENSITY AND MODULARITY", self.densityList.mean(), self.modularityList.mean()

        return stateDict

#start process
if __name__ == '__main__':
    with open('pickleDumps/objs.pkl') as f:
        timesteps, timeSeriesData = pickle.load(f)




import numpy as np
import networkx as nx
# import bct
import community as cm 
from colorBrewer import *
import pprint
from collections import defaultdict
from Correspondences import Correspondence
import numpy as np
from scipy.signal import argrelextrema
from modelAverageGraphs import modelAverageGraphs
from hierarchicalTimeNodeDataStructure import Node
from collections import Counter
import pickle

PosFilename = "sampleData/ESNeTData/PosMatrix.npy"
ESNETdata = False
PosFilename = "sampleData/primarySchools/positions.csv"

class CommunityDataProcessing(object):
    def __init__(self):
        self.communityData = None
        self.timestepPartition = None
        self.first = False

    def thresholdGraphValues(self, data, weight = 0.0):
        ThresholdData = np.copy(data)
        low_values_indices = ThresholdData < weight  # Where values are low
        ThresholdData[low_values_indices] = 0
        return nx.from_numpy_matrix(ThresholdData)  

    def modelGraph(self, numpyGraphData, timesteps, thresholdWeight):
        thresholdData = np.copy(numpyGraphData[timesteps])
        return self.thresholdGraphValues(thresholdData, thresholdWeight)

    def definePositions(self, communityGraph, prog):
        import csv 
        posDict = dict()

        with open(PosFilename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                posDict[int(row[0])] = np.array([float(row[1])*0.4,float(row[2])*0.4])

        return posDict
        # return nx.spring_layout(communityGraph, scale= 0.66)

    def defineReducedPositions(self,graph, interval, prog):
        return self.definePositions(graph, prog)

    def defineCommunities(self, communityGraph, data, threshold, modularitylevel):
        newdata = np.array(data)
        partition = dict()
        partition= cm.best_partition(communityGraph)
        modularity = cm.modularity(partition,communityGraph)
        density = nx.density(communityGraph)
        clustering = nx.clustering(communityGraph)
        avg_clustering = nx.average_clustering(communityGraph)
        """
        The value has to be nodes edges and containment information
        for the layout to work in such a manner
        """
        induced_graph = cm.induced_graph(partition, communityGraph)
        numpyMat = nx.to_numpy_matrix(induced_graph)

        centrality = nx.degree_centrality(communityGraph)
        load_centrality = nx.load_centrality(communityGraph)
        betweenness_centrality = nx.betweenness_centrality(communityGraph)
        closeness_centrality = nx.closeness_centrality(communityGraph)

        characteristicPathLength = []
        for g in nx.connected_component_subgraphs(communityGraph): 
            try:
                characteristicPathLength.append(nx.average_shortest_path_length(g))
            except ZeroDivisionError:
                pass
        return (density, partition, modularity, clustering, avg_clustering, np.mean(characteristicPathLength),centrality, load_centrality, betweenness_centrality, closeness_centrality, induced_graph, numpyMat)

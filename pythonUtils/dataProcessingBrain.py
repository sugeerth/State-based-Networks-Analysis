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
from CommunityDataProcessing import CommunityDataProcessing
from collections import Counter
from loadDatasets import loadDataSets
from JSONobjectsForData import JSONobjectsForData
from clusterDistanceMatrix import clusterDistanceMatrix 
import pickle

"""
This is the data that needs to be changed based on the format of the data
"""

TimeWindow = 0

THRESHOLDVALUE = 0.00
# labelFilename = "sampleData/JesseData/roi_names_21.txt" 
# BrainLabels = "sampleData/JesseData/roi_names_21.txt" 

ESNETlabelFilename = "sampleData/ESNeTData/roi_33_names.txt"
ESNETPosFilename = "sampleData/ESNeTData/PosMatrix.npy"
ESNETUTCTime= "sampleData/ESNeTData/UTCTimeLabels.txt" 

DBLPlabelFilename = "sampleData/Citation_Data/roi_dblp_authors.txt"
CITATION_YEAR = "sampleData/Citation_Data/roi_dblp_year.txt"

EmailEUCorelabelFilename = "sampleData/EUCoreData/roi_eu_core_ids.txt" 
EmailEUCoreYEAR = "sampleData/EUCoreData/roi_time_manual.txt" 

PrimarySchoolslabelFilename = "sampleData/primarySchools/labels.txt" 

SIMILARITY_THRESHOLD = 0.0

class dataProcessing(object):
    def __init__(self,filename):

        self.GlobalmaxTopologicalOverlap = -999
        self.GlobalminTopologicalOverlap = 999

        self.GlobalmaxGlobalOverlap = -999
        self.GlobalminGlobalOverlap = 999

        self.communityObject = CommunityDataProcessing()
        self.filename = filename

        """
            Add the dataset objects in here
        """        
        self.loadDataSets =  loadDataSets(filename, self)
        self.clusterDistanceMatrixObject = clusterDistanceMatrix(self)
        self.JSONObjects = JSONobjectsForData(self)

        # Jesse's Dataset 
        # self.FileLabels = self.loadDataSets.loadLabels(BrainLabels)
        # self.matRenderData = self.loadDataSets.loadSyntheticDatasets()

        # ESNET Network Flow Dataset
        # self.FileLabels = self.loadDataSets.loadESNETLabels(ESNETlabelFilename)
        # self.matRenderData = self.loadDataSets.loadESNETDataset(ESNETPosFilename)
        # self.TimeLabels = self.loadDataSets.loadUTCTimeLabels(ESNETUTCTime)

        # DBLP dataset
        # self.FileLabels = self.loadDataSets.loadESNETLabels(DBLPlabelFilename)
        # self.matRenderData = self.loadDataSets.loadDBLPDataset(filename)
        # self.TimeLabels = self.loadDataSets.loadDBLPTimeLabels(CITATION_YEAR)

        # Email EU Core dataset
        # self.FileLabels = self.loadDataSets.loadESNETLabels(EmailEUCorelabelFilename)
        # self.matRenderData = self.loadDataSets.loadEUCoreDataset(filename)
        # self.TimeLabels = self.loadDataSets.loadEUTimeLabels(EmailEUCoreYEAR)

        # Primary School dataset
        self.FileLabels = self.loadDataSets.loadPrimarySchoolLabels(PrimarySchoolslabelFilename)
        self.matRenderData = self.loadDataSets.loadPrimarySchoolDataset(filename)
        self.nodeLength = len(self.matRenderData[1])

        # Dan's Dataset 
        # self.matRenderData = self.loadDataSets.loadDansDataset()

        # McFarlands's Dataset 
        # self.matRenderData = self.loadDataSets.loadMcFarlandsDataset()

        self.length = len(self.matRenderData[0])
        self.max, self.min = round(np.amax(self.matRenderData),2),  round(np.min(self.matRenderData),2)
        self.maxTimeSteps = len(self.matRenderData)-1

        self.communityHashmap = dict()
        self.communityHierarchy = dict()
        self.NodePositions = dict()
        
        self.summaryIntervalValues = dict()

        self.modularityList = np.zeros((self.maxTimeSteps))
        self.densityList = np.zeros((self.maxTimeSteps))
        self.NodeLevels = dict()

        self.corres = Correspondence(self)

        """
            Caching datasets in a list and putting them into a list
        """        
        self.square_clusteringList = np.zeros((self.maxTimeSteps))
        self.distanceMatrix = np.zeros((self.maxTimeSteps,self.maxTimeSteps))
        self.avg_clusteringList = np.zeros((self.maxTimeSteps))
        self.characteristicPathLengthList = np.zeros((self.maxTimeSteps))
        self.centralityList = np.zeros((self.maxTimeSteps, self.nodeLength))
        self.clusteringList = np.zeros((self.maxTimeSteps, self.nodeLength))
        self.BetweennessList = np.zeros((self.maxTimeSteps, self.nodeLength))
        self.load_centralityList = np.zeros((self.maxTimeSteps, self.nodeLength))
        self.closeness_centralityList = np.zeros((self.maxTimeSteps, self.nodeLength))
        self.induced_graphList = []
        self.NumpyMatList = []

        """
            Store the average graphs so that you can better understand what the graphs are
        """
        self.averageGraphs = modelAverageGraphs(self) 

        self.graphDataStructureList = dict()      
        self.timestepNetworkData = []
        self.colorNetworkData = [] 
    
        self.first = True
        self.thresholdWeight = THRESHOLDVALUE
        self.modularityLevel = 1

        # Here we have changes in the graph where we compute how new things are formed
        self.thresholdData = self.newThresholdCompute(self.thresholdWeight, self.modularityLevel)

    def newThresholdCompute(self, value, level, toggleValue = False):
        self.timeSeriesData = []
        self.nodePositions = dict()
        self.thresholdWeight = value
        self.modularityLevel = level
        self.globalMetricValue = None
        self.globalGraphNetworkxData = dict()
        self.differenceData = []
        self.summaryDifferenceData = []
        self.globalEdgeBetweennessDifference = dict()

        self.first = True
        for i in range(self.loadDataSets.timesteps_for_dataProcessingBrain):
            self.timeSeriesData.append(self.JSONObjects.formatToJSON(self.matRenderData, i,toggleValue))
            if i > 0:
                self.corres.findCorrespondence(self.timeSeriesData[i],self.timeSeriesData[i-1], i) 
                self.differenceData.append(self.JSONObjects.formatToDifferenceJSON(i, self.timeSeriesData[i-1], self.timeSeriesData[i], self.globalGraphNetworkxData[i-1],self.globalGraphNetworkxData[i], toggleValue))

        self.loadDataSets.writeFile("saved")

        # Define similarity matrix based on the metrci of the given choice
        self.distanceMatrix = self.clusterDistanceMatrixObject.defineDistanceMatrixForVisualization(self.loadDataSets.timesteps_for_dataProcessingBrain, self.timeSeriesData, self.corres, TimeWindow, self.distanceMatrix)
     
        # Clustering Matrix Based approach, Identifying the intervals there! 
        states = self.clusterDistanceMatrixObject.clusterDistanceMatrix(self.distanceMatrix)
 
        # States using Local Maxima and Minima Approach
        # states1 = self.identifyLocalMaxima()

        # Identify a hierarchy of states that we can use to visualize the data
        self.stateHierarchy = self.clusterDistanceMatrixObject.deriveHierarchicalStructure(states)

        # Write the data for the visualization in the matrix
        self.clusterDistanceMatrixObject.writeSimilarityValuesForVisualization(self.distanceMatrix)

        #return self.timeSeriesData, states, self.differenceData 
        return self.timeSeriesData, self.differenceData, states

    def defineReducedNodePositions(self, interval, prog):
        # FIX ME changing the interval value to 0 
        positions = self.communityObject.definePositions(self.graphDataStructureList[0], prog)
        return positions

    def getRenderingDataForSummaryGraph(self, root, toggleValue):
        self.timeSeriesSummaryGraph = dict()
        timeSeriesSummaryGraph = []
        first = True
        intervalList = []

        self.intervalForSummaryDifference = []
        self.NodeSummaryPositionsDict = dict()

        for j in range(self.levels):
            listIndex = list()
            for index, i  in enumerate(self.NodeLevels[j]):
                listIndex.append(self.defineReducedNodePositions(0, "fdp"))
            self.NodeSummaryPositionsDict[j] = listIndex

        for j in range(self.levels):
            networkDataList = []
            self.timeSeriesSummaryGraph[j] = networkDataList
            for indexLevels, i in enumerate(self.NodeLevels[j]):
                dataFound = False
                for index, data in enumerate(intervalList):
                    if data == (i.interval[0],i.interval[1]):  
                        timeSeriesSummaryGraph.append(timeSeriesSummaryGraph[index])
                        networkDataList.append(timeSeriesSummaryGraph[index])
                        intervalList.append((i.interval[0],i.interval[1]))
                        dataFound = True
                        break
                if dataFound: 
                    continue
                if first: 
                    NodeSummaryPositions = self.communityObject.definePositions(i.reducedNetworkxGraph, "fdp")
                    first = False
                JSONdata = self.JSONObjects.formatAverageGraphs(indexLevels,0,i,i.interval[0],i.interval[1], i.reducedNetworkxGraph,i.reducedMatrix, i.reducedCommunityAssignments,self.NodeSummaryPositionsDict[j][indexLevels],toggleValue)
                timeSeriesSummaryGraph.append(JSONdata)
                networkDataList.append(JSONdata)
                intervalList.append((i.interval[0],i.interval[1]))
                #FIXME
                if j == 1: 
                    self.intervalForSummaryDifference.append((i.interval[0],i.interval[1]))
        return self.timeSeriesSummaryGraph

    def getRenderingDataForDifferenceToSummaryGraph(self,length, summaryGraphs, toggleValue):
        """
        This function gets the relvant data for the topology of difference from Summary to difference data
        There is a bug with the "j" in the summary grpahs
        """
        lastj = 0
        
        for i in range(self.loadDataSets.timesteps_for_dataProcessingBrain):
            j = self.findSummaryGraphIndex(i, summaryGraphs,lastj)
            try: 
                self.summaryDifferenceData.append(self.JSONObjects.formatToDifferenceJSON(i,self.timeSeriesData[i],summaryGraphs[j], self.globalGraphNetworkxData[i],self.NodeLevels[length][j].reducedNetworkxGraph, toggleValue))
            except IndexError: 
                pass
            lastj = j
        return self.summaryDifferenceData

    def findSummaryGraphIndex(self, valueOfTimestep,summaryGraphs, lastj):
        counter = 0 
        for start,end in self.intervalForSummaryDifference: 
            if valueOfTimestep >= start and valueOfTimestep <= end:
                return counter
            counter = counter+1
        return lastj



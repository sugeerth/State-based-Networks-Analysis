
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
import pickle
# import Pycluster

"""
This is the data that needs to be changed based on the format of the data
"""

NODES = 242
TIMESTEPS = 201 

timesteps = 101

THRESHOLDVALUE = 0.00

class loadDataSets(object):
    def __init__(self, filename, object1):
        self.filename  = filename
        self.dataProcessinObject = object1 
        global timesteps
        self.timesteps_for_dataProcessingBrain = timesteps - 1 

    def loadSyntheticDatasets(self): 
        """
        Loads the enron dataset into the datastructure to show graphData == 0--10 timesteps with nodes, edges and 
        changes in graphs. 
        Idea to find out how the community structure changes and what happens 
        to the overall topology
        """
        with open(self.filename) as f: 
            i = 0 
            counter = 0
            arraylist = np.zeros((TIMESTEPS,NODES,NODES),dtype=np.float64)
            for line in f: 
                line = line.strip()
                data = np.array(map(float,line.split(' ')))
                for k,data1 in enumerate(data):
                    if counter== 0 and i == 1 and k ==0:
                        savedValue = data1
                    arraylist[counter][i][k] = np.float64(data1)
                i = i+1 
                if (i == 21):
                    counter = counter+1
                    i = 0

        # Slicing changes in the graph
        arraylist = arraylist[0:timesteps,:,:]
        
        return arraylist

    """
    Testing two types of datasets that can be loaded here. 
    Both are better off here 
    """
    def loadDBLPDataset(self, filename):
        arraylist =  np.load(self.filename)
        return arraylist

    def loadDBLPTimeLabels(self,filename):
        import csv
        labels = []

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\n')
            for row in reader:
                labels.append(row[0])  
                  
        return labels  
    
    def loadEUCoreDataset(self, filename):
        arraylist =  np.load(self.filename)
        return arraylist

    def loadEUTimeLabels(self,filename):
        import csv
        labels = []

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\n')
            for row in reader:
                labels.append(row[0])  
                  
        return labels 
        
    def loadESNETLabels(self, filename):
        """
        Load the labels here
        """
        import csv
        labels = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\n')
            for row in reader:
                labels.append(row[0])    
        return labels

    def primarySchoolsData(self, filename):
        arraylist =  np.load(self.filename)

        # Slicing changes in the graph
        arraylist = arraylist[0:timesteps,:,:]
        
        return arraylist

    def understandDansData(self, filename):
        arraylist =  np.load(filename)
        arraylist = arraylist[12:]
        arraylist = arraylist[FIRSTOFFSET:]
        arraylist = arraylist[:-LASTOFFSET or None]

        low_values_indices = arraylist <  THRESHOLDVALUE # Where values are low
        arraylist[low_values_indices] = 0  # All low values set to 0

        return (arraylist, len(arraylist), len(arraylist)) 

    def loadPrimarySchoolDataset(self, filename): 
        arraylist =  np.load(self.filename)

        # Slicing changes in the graph
        arraylist = arraylist[0:timesteps,:,:]

        return arraylist


    def loadPrimarySchoolLabels(self, filename):
        """
        Loading the PrimarySchools Files
        """
        counter = 0 
        node_lookup = [] 

        with open(filename, 'r') as outfile: 
            for index, l in enumerate(outfile):
                    node, label1, label2 = l.strip().split("\t")
                    node_lookup.append(label1)
        return node_lookup

    def loadESNETLabels(self, filename):
        """
        Load the labels here
        """
        import csv
        labels = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\n')
            for row in reader:
                labels.append(row[0])    
        return labels

    def loadUTCTimeLabels(self, filename):
        """
        Loads the time Labels so the visualizations can show what is changing and what is not?
        """
        import csv
        labels = []

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\n')
            for row in reader:
                labels.append(row[0])  
        return labels


    def writeFile(self,answer):
        with open('communityHashmap.pkl', 'wb') as f:
            change = pickle.dump(self.dataProcessinObject.globalCommunityHashmap, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('colors.pkl', 'wb') as f:
            change = pickle.dump(self.dataProcessinObject.colorNetworkData,  f, protocol=pickle.HIGHEST_PROTOCOL)


    def loadLabels(self):
        """
        Load the labels here
        """
        import csv
        labels = []
        with open(labelFilename, 'r') as f:
            reader = csv.reader(f, delimiter='\n')
            for row in reader:
                labels.append(row[0])    
        return labels
import numpy as np
import networkx as nx
import community as cm 
from collections import defaultdict

"""
This is the data that needs to be changed based on the format of the data
"""

class Node(object):
    def __init__(self, interval1, interval2, level):
        self.interval = (interval1, interval2)
        self.children = []
        self.reducedNetworkxGraph = []
        self.reducedMatrix = []
        self.reducedCommunityAssignments = []
        self.reducedNodePositions = []
        self.level = level

    def add_child(self, obj):
        self.children.append(obj)

    def lookupNodetoBeAdded(self, interval):
    	for i, childInterval in enumerate(self.children):
    		if interval[1] <= childInterval.interval[1] and interval[0] >= childInterval.interval[0]:
    			break
        return self.children[i]
    
    def hasChildNodes(self, counter):
    	if self.children[counter].children == None: 
    		return False
		return True



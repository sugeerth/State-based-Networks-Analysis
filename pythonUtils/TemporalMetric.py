import numpy as np
import networkx as nx
# import bct
import community as cm 
import pprint
import copy
from colorBrewer import *
from collections import defaultdict
"""
This is the data that needs to be changed based on the format of the data
"""

timesteps = 204
nodes = 21 
THRESHOLDVALUE = 0.40

class TemporalMetric(object):
	def __init__(self, correspondenceBrainObject):
		self.colorsThresholdValue = 0.20



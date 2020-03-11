import networkx as nx
import scipy

"""
This is the data that needs to be changed based on the format of the data
"""

import numpy as np
import math
import colorsys

"""
Identifying changes in visualizatio n


"""
def DistanceForBrainRegions(G, nodelist=None, weight='weight'):
    import scipy.sparse
    if nodelist is None:
        nodelist = G.nodes()
    A = nx.to_scipy_sparse_matrix(G, nodelist=nodelist, weight=weight,
                                  format='csr')
    n,m = A.shape
    diags = A.sum(axis=1)
    D = scipy.sparse.spdiags(diags.flatten(), [0], m, n, format='csr')
    return D 


def CSRMax(CSRDData,length):
	max1 = -999
	for i in range(length):
		if max1 < CSRDData[(i,i)]: 
			max1 = CSRDData[(i,i)]
	return max1

def RootSim(PFinalMatrix, NFinalMatrix):
	x = len(PFinalMatrix)
	y = len(NFinalMatrix[0]) 
	sum1 = 0

	for i in range(x):
		for j in range(y):
			sum1 = sum1 + (math.sqrt(PFinalMatrix[i,j]) - math.sqrt(NFinalMatrix[i,j]))**2 

	return math.sqrt(sum1)
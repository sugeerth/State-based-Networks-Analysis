import numpy as np
import networkx as nx
import community as cm 
from colorBrewer import *
import pprint
from collections import defaultdict
import numpy as np
from scipy.signal import argrelextrema
from collections import Counter
import pickle


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class JSONobjectsForData(object):
    def __init__(self, object1):
        self.communityData = None
        self.dataProcessingObject = object1
        self.timestepPartition = None
        self.first = False

    def formatToJSON(self, data, timestep, toggleValue= False): 
        self.nodelist = [] 
        self.edgelist = []
        self.grouplist = []
        self.groupViz = []

        if timestep == 0: 
            firstNode = True
            self.dataProcessingObject.timestepNetworkData = [] 
            self.dataProcessingObject.globalCommunityHashmap = []
            self.dataProcessingObject.colorNetworkData = []
        else:
            firstNode = False

        width =300
        height=300
        
        XOffset = 80
        YOffset = 50

        graphForCommunity = self.dataProcessingObject.communityObject.modelGraph(data, timestep, self.dataProcessingObject.thresholdWeight) 
        thresholdData = nx.to_numpy_matrix(graphForCommunity)
        self.dataProcessingObject.timestepNetworkData.append(thresholdData)
        
        self.dataProcessingObject.graphDataStructureList[timestep] = graphForCommunity
        density, communityHashmap, modularity, clustering, avg_clustering, characteristicPathLength, centrality, load_centrality, Betweenness, closeness_centrality,induced_graph,numpyMat= self.dataProcessingObject.communityObject.defineCommunities(graphForCommunity,thresholdData, self.dataProcessingObject.thresholdWeight, self.dataProcessingObject.modularityLevel) 
        
        self.dataProcessingObject.globalCommunityHashmap.append(communityHashmap)
        self.dataProcessingObject.globalGraphNetworkxData[timestep] = graphForCommunity
        self.dataProcessingObject.modularityList[timestep] =  modularity
        self.dataProcessingObject.NumpyMatList.append(numpyMat)
        self.dataProcessingObject.densityList[timestep] = density
        self.dataProcessingObject.avg_clusteringList[timestep] = float(avg_clustering)
        self.dataProcessingObject.characteristicPathLengthList[timestep]= characteristicPathLength
        self.dataProcessingObject.centralityList[timestep] = centrality.values()
        self.dataProcessingObject.load_centralityList[timestep] = load_centrality.values()
        self.dataProcessingObject.BetweennessList[timestep] = Betweenness.values()
        self.dataProcessingObject.clusteringList[timestep] = clustering.values()

        centrality = nx.degree_centrality(graphForCommunity)
        
        edgeBetweenness = nx.edge_betweenness_centrality(graphForCommunity, normalized=True, weight='weight')
        self.dataProcessingObject.globalEdgeBetweennessDifference[timestep] = edgeBetweenness

        colorsC = map(hex_to_rgb, qualitative['Set3'][256]) 
        
        if self.dataProcessingObject.first: 
            self.dataProcessingObject.NodePositions = self.dataProcessingObject.communityObject.definePositions(graphForCommunity, "fdp")
            self.dataProcessingObject.first = False

        timeData = dict()
        nodeDict = dict()
        edgeDict = dict()
        groupDict= dict()
    
        color = [] 
        # Identify Island communities and color them 
        # grey so that they do not interfere with color flow

        communityMultiple = defaultdict(list)

        for node, group in communityHashmap.items():
            communityMultiple[group].append(node)

        islandCommunities = self.findIslandCommunities(communityMultiple)
        for i in range(0,len(data[timestep])):
            nodeDict = dict()
            
            if firstNode:
                if communityHashmap[i] in islandCommunities: 
                    nodeDict["color"] = "rgb(122,122,122)"
                else:
                    nodeDict["color"] = "rgb("+str(colorsC[communityHashmap[i]-1])+")"

            nodeDict["node"] = i
            nodeDict["timestep"] = timestep           
            nodeDict["group"] = communityHashmap[i]

            # nodeDict["width"] = 0
            # nodeDict["height"] = 0

            # if toggleValue:
            # self.NodeSummaryPositionsDict[2][]
            # print self.NodeSummaryPositionsDict[2][0]

            X = XOffset+ float(self.dataProcessingObject.NodePositions[i][0]*width)
            Y = YOffset+ float(self.dataProcessingObject.NodePositions[i][1]*height)
            
            nodeDict["x"] = format(X,'.2f')
            nodeDict["y"] = format(Y,'.2f')
            nodeDict["fixed"] = "true"
            nodeDict["centrality"] = "{0:.2f}".format(centrality[i])
            # nodeDict["betweenness_centrality"] = "{0:.2f}".format(betweenness_centrality[i])
            # nodeDict["load_centrality"] = "{0:.2f}".format(load_centrality[i])

            self.nodelist.append(nodeDict)
            self.grouplist.append(communityHashmap[i])
            self.groupViz.append(groupDict)

        for l in range(0,len(data[timestep]-1)):
            for m in range(0,len(data[timestep]-1)):
                value = round(data[timestep][l][m],1)

                if value < self.dataProcessingObject.thresholdWeight:
                    continue

                if value < 0:
                    signed = 1  
                elif value > 0: 
                    signed = 0  
                else: 
                    continue
                edgeDict = dict()
                edgeDict["signed"] = signed

                #try: 
                #    edgeDict["edgeBetweennessCentrality"] = "{0:.2f}".format(edgeBetweenness[(l,m)]*10)
                #except KeyError: 
                #    edgeDict["edgeBetweennessCentrality"] = "-1"

                edgeDict["source"] = l
                edgeDict["target"] = m
                edgeDict["value"] = round(data[timestep][l][m],2)
                self.edgelist.append(edgeDict)

        if firstNode:
            color = [] 
            # Identify Island communities and color them 
            # grey so that they do not interfere with color flow

            communityMultiple = defaultdict(list)

            for node, group in communityHashmap.items():
                communityMultiple[group].append(node)

            islandCommunities = self.findIslandCommunities(communityMultiple)
           
            for nodeId, i in enumerate(self.nodelist): 
                if nodeId in islandCommunities:
                    color.append('rgba(199,199,199,0.9)')
                    i["color"] = 'rgba(199,199,199,0.9)'
                else: 
                    color.append(i["color"])

            timeData["colors"] = color
            self.dataProcessingObject.colorNetworkData.append(color)

        timeData["nodes"] = self.nodelist
        timeData["links"] = self.edgelist

        #timeData["groups"] = self.grouplist
        #timeData["density"] = density
        
        #timeData["clustering"] = clustering
        #timeData["centrality"] = centrality
        #timeData["Betweenness"] = Betweenness
        #timeData["load_centrality"] = load_centrality
        #timeData["closeness_centrality"] = closeness_centrality

        #timeData["average_clustering"] = avg_clustering
        #timeData["characteristicPathLength"]= characteristicPathLength

        timeData["modularity"] = modularity
        return timeData

    def formatToDifferenceJSON(self, timeStep, previousData, currentData, previousNetworkx, currentNetworkx, toggleValue= False):
        """
        The purpose of this is to determine where the changes are and how we identify these changes.
        find the difference between current and prevous data 

        Attributes" 
        1) Change in communities
        2) Change in edgeWeights 
        3) Change in edgeLength
        4) Change in the edgeImportance 
        """ 
        nodelist = [] 
        edgelist = []

        width = 300
        height = 300
        
        XOffset = 80
        YOffset = 50

        timeData = dict()
        nodeDict = dict()
        edgeDict = dict()
        groupDict= dict()

        length = len(self.dataProcessingObject.matRenderData[timeStep])
        a = self.dataProcessingObject.globalGraphNetworkxData[timeStep]

        a = currentNetworkx
        b = previousNetworkx

        sym_Diff = nx.symmetric_difference(a,b)
    
        for i in range(0,len(self.dataProcessingObject.matRenderData[timeStep])):
            nodeDict = dict()
            color = []
            nodeDict["node"] = i
            # nodeDict["centralityChange"] = "{0:.2f}".format(currentData["centrality"][i] - previousData["centrality"][i])  
            # nodeDict["BetweennessChange"] = "{0:.2f}".format(currentData["Betweenness"][i] - previousData["Betweenness"][i]) 
            
            if (previousData["nodes"][i]["color"] == currentData["nodes"][i]["color"]):
                color = currentData["nodes"][i]["color"]
            else:
                color = [previousData["nodes"][i]["color"], currentData["nodes"][i]["color"]]
            nodeDict["color"] = color 
            nodeDict["opacityValue"] = 0.2

            # if toggleValue:
                # self.NodeSummaryPositionsDict[2][]
                # print self.NodeSummaryPositionsDict[2][0]
            

            X = XOffset+ float(self.dataProcessingObject.NodePositions[i][0]*width)
            Y = YOffset+ float(self.dataProcessingObject.NodePositions[i][1]*height)
            
            nodeDict["x"] = format(X,'.2f')
            nodeDict["y"] = format(Y,'.2f')
            nodeDict["timestep"] = timeStep           
            nodeDict["fixed"] = "true"

            nodelist.append(nodeDict)

        for l,m in sym_Diff.edges():
                diffValue = round(self.dataProcessingObject.matRenderData[timeStep][l][m],2) - round(self.dataProcessingObject.matRenderData[timeStep-1][l][m],2)

                if diffValue < 0:
                    signed = 1  
                elif diffValue > 0: 
                    signed = 0  
                else: 
                    continue

                edgeDict = dict()
                edgeDict["signed"] = signed

                edgeDict["source"] = l
                nodelist[l]["opacityValue"] += 0.2

                if (nodelist[l]["opacityValue"]) > 1: 
                    nodelist[l]["opacityValue"] = 1
                
                edgeDict["target"] = m
                
                nodelist[m]["opacityValue"] += 0.2
                if (nodelist[m]["opacityValue"]) > 1: 
                    nodelist[m]["opacityValue"] = 1

                edgeDict["value"] = diffValue
                edgelist.append(edgeDict)

        timeData["nodes"] = nodelist
        timeData["links"] = edgelist

        return timeData
    
    def formatAverageGraphs(self, index, level,childObject, interval1,interval2, graphForCommunity, thresholdData, communityColorHashmap, NodeSummaryPositions, toggleValue= False): 
        self.nodelist = [] 
        self.edgelist = []

        width =300
        height=300
        
        XOffset = 80
        YOffset = 50

        # print childObject.storageMatrix
        # print childObject.reducedVarianceMatrix, "reduced Matrix" 

        length = len(childObject.topTimeSteps)
        newDict = dict()
        newnewDict = dict()
        for k, v in childObject.distributionOfCommunityAssignments.items():
            newDict = dict()
            for k1,v1 in v.items():
                newDict[k1] = format(v1/float(length),'.2f')
            newnewDict[k] =  newDict

        centrality = nx.degree_centrality(graphForCommunity)
        edgeBetweenness = nx.edge_betweenness_centrality(graphForCommunity, normalized=True, weight='weight')
        # edgeBetweenness = nx.edge_current_flow_betweenness_centrality(graphForCommunity, normalized=True, weight='weight')

        # partitionForVerification= cm.best_partition(graphForCommunity)

        communityHashmap= self.convertCommunityColorHashmaptoIntegers(communityColorHashmap)
        # induced_graph = cm.induced_graph(communityHashmap, graphForCommunity)
        # numpyMat = nx.to_numpy_matrix(induced_graph)

        timeData = dict()
        nodeDict = dict()
        edgeDict = dict()
    
        for i in range(0,len(graphForCommunity.nodes())):
            nodeDict = dict()

            nodeDict["node"] = i
            # nodeDict["timestepInterval"] = (interval1,interval2)           
            # if toggleValue: 
                # X = XOffset+ float(NodeSummaryPositions[i][0]*width)
                # Y = YOffset+ float(NodeSummaryPositions[i][1]*height)    
            X = XOffset+ float(self.dataProcessingObject.NodePositions[i][0]*width)
            Y = YOffset+ float(self.dataProcessingObject.NodePositions[i][1]*height)    
            nodeDict["x"] = format(X,'.2f')
            nodeDict["y"] = format(Y,'.2f')
            nodeDict["fixed"] = "true"

            nodeDict["centrality"] = "{0:.2f}".format(centrality[i])
            nodeDict["color"] = communityColorHashmap[i]
            nodeDict["colorDist"] = newnewDict[i]
            nodeDict["timestep"] = index          

            self.nodelist.append(nodeDict)

        varianceThr = []
        for l in range(0, len(graphForCommunity.nodes())):
            for m in range(0, len(graphForCommunity.nodes())):
                data = thresholdData[l,m]

                value = round(data,2)

                if value < self.dataProcessingObject.thresholdWeight:
                    continue
                variance = childObject.reducedVarianceMatrix[l,m]
                storageMatrix = childObject.reducedVarianceMatrix[l,m]

                edgeValues = list()
                for i in range(len(childObject.topTimeSteps)):
                    edgeValues.append(round(childObject.storageMatrix[i,l,m],3))

                variance = round(variance,8)

                if value < 0:
                    signed = 1  
                elif value > 0: 
                    signed = 0  
                else: 
                    continue

                edgeDict = dict()
                edgeDict["signed"] = signed

                edgeDict["source"] = l
                edgeDict["target"] = m
                edgeDict["value"] = value
                edgeDict["variance"] = variance * 100
                varianceThr.append(variance * 100)
                edgeDict["edgesList"] = edgeValues

                self.edgelist.append(edgeDict)

        meanV = np.mean(varianceThr)
        stdV =  np.std(varianceThr)
        timeData["colors"] = communityColorHashmap
        timeData["varianceThreshold"] = meanV + stdV
        timeData["colorDistribution"] = newnewDict
        timeData["intervals"] = [interval1,interval2]
        timeData["nodes"] = self.nodelist
        timeData["associatedData"] = list(childObject.topTimeSteps)
        timeData["links"] = self.edgelist
        timeData["level"] = level
        return timeData

    def findIslandCommunities(self, communityMultiple):
        island = list()
        for group, nodes in communityMultiple.items():
            if len(nodes) == 1: 
                island.append(nodes[0])
        return island

    def convertCommunityColorHashmaptoIntegers(self, partition):
        communityMultiple = defaultdict(list)
        
        community = dict()
        hashmap = dict()

        counter = 0

        for i in set(partition.values()):
            hashmap[i] = counter    
            counter = counter + 1

        for i,j in partition.items():
            community[i] = hashmap[j]

        return community



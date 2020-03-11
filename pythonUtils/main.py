import os
import os.path as path
from dataProcessingBrain import dataProcessing


brainDataNetwork = None
brainDataObject = None

# filename = "../sampleData/EUCoreData/timeVaryingData.npy"
filename = "../sampleData/primarySchools/timeVaryingData.npy"

class mainModel(object):
    def __init__(self):
        CURR =  path.abspath(path.join(__file__ ,"..")) # going one directory up 
        CURR =  os.path.join(CURR, filename)

        self.brainDataObject = dataProcessing(CURR)

        self.brainDataNetwork = self.brainDataObject.timeSeriesData
        self.differenceData = self.brainDataObject.differenceData
        self.averageGraphs = []
        self.maxTimeSteps=self.brainDataObject.maxTimeSteps
        self.modularitylevel = 1
        self.FileLabels = self.brainDataObject.FileLabels

        print self.maxTimeSteps
        print str(self.brainDataNetwork).replace("'", '"')
        print str(self.differenceData).replace("'", '"')

        toggleNodePositions = False

        # Takes the state information and then tries to identify the major average graphs that can be used for analysis
        self.averageGraphs = self.brainDataObject.averageGraphs.returnModelledAverageGraphsObject(self.brainDataObject.thresholdData[2])
        self.summaryBrainNetworkData = self.brainDataObject.getRenderingDataForSummaryGraph(self.averageGraphs,toggleNodePositions)

        # self.averageGraphs = [] 
        # self.summaryBrainNetworkData = []

        print str(self.summaryBrainNetworkData).replace("'", '"')
        print str(self.brainDataObject.thresholdData[2])
        print str(self.brainDataObject.NodeSummaryPositionsDict).replace("'", '"')
        print str(self.brainDataObject.FileLabels).replace("'", '"')


def main():
    self = mainModel()

#start process
if __name__ == '__main__':
    main()



# Difference Visualization With a Novel Context Analysis Graph for Interconnect Data 
Please click to watch the overview video
 
 [![SummaryAndDifferenceGraphRealData.png](https://s9.postimg.org/uix421yq7/Summary_And_Difference_Graph_Real_Data.png)](https://vimeo.com/211385432)
 
<!--  [![ScreenShot](https://github.com/sugeerth/ECoG-ClusterFlow/blob/FinalWorkingTool/src/Images/Uload.png)](https://vimeo.com/175328739)
======= -->

# DyNet #
The advent of recording technologies has given rise to large amounts of rich temporal graph-structured data in many applications. The analysis of such complex networks is challenging due to its complex time-varying behavior. In an internet graph, for example, communications patterns between computers frequently change, hubs or routers change roles transtitioning the entire topology of the entire network. To clearly understand the effect of such temporal changes, we need methods that not only identify changes but also reveal the topological effect the changes have on the network. In this paper, we present a novel difference graph approach for network analysis, that visualizes and reveals the topological effect that a change brings about in a network. We introduce an umbrella metaphor to determine how low-level changes in the graph change the community structure of the graph. We further introduce interaction and visual design techniques to reveal the holistic changes between subsequent graphs. Our method is complemented by interactive techniques that reveal holistic changes describing the cause and effect of topological properties of graphs. We apply our algorithm to two datasets, an internet dataset and a network data set. 

### Required dependencies ###
	  numpy
	  networkx 
	  community


### Getting Started  ###
Note: Tested on OS X 10.11.6 and Ubuntu 14.04

	  pip install flask
	  pip install numpy
	  pip install networkx
	  pip install community
	  pip install bctpy
	  pip install colorBrewer
	  pip install networkx
	  python main.py

	#Download TimeSum repository and then goto src folder 
	
	DyNET/src> main.py 
		Happy Analysis! 
        
Contributing
------------

See [Contributing](CONTRIBUTING.md)

### Citation Information###
Please cite TimeSum in your publications if it helps your research:
 
The TimeSum Project makes use of the following libraries
* [Numpy](https://pypi.python.org/pypi/numpy/1.11.0), Copyright (C) 2004-2016, NetworkX is distributed with the BSD license
* [PYTHON LOUVAIN](https://pypi.python.org/pypi/python-louvain), Copyright (c) 2009, Thomas Aynaud <thomas.aynaud@lip6.fr>

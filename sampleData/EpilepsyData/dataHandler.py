name1 = "ConsensusCluster04.json"
name2 = "ConsensusCluster14.json"
 
import pickle 

timestepPartition1 = pickle.load(open(name1))
timestepPartition2 = pickle.load(open(name2))


partition1 = timestepPartition1[10]
partition2 = timestepPartition2[10]

print set(partition1.values()), set(partition2.values())

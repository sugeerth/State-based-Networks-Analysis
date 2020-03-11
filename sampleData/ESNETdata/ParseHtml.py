import numpy as np 

file = open("PosFiles.txt", "r") 


Max1 = -99999
Min1 = 9999

Max2 = -99999
Min2 = 9999

from collections import defaultdict
NationalLabs = defaultdict(list)
for line in file:
	line= line.strip()
	line = line.split(" ")
	line[0]= line[0].replace('"','')
	line[1]= line[1].replace('"','')

	if Max1 < float(line[0]): 
		Max1= float(line[0])

	if Max2 < float(line[1]): 
		Max2= float(line[1])

	if Min1 > float(line[0]): 
		Min1= float(line[0])

	if Min2 > float(line[1]): 
		Min2= float(line[1])

	x = (float(line[0]) -90.6666)/(1108.0-90.6666) 
	y = (float(line[1]) - 56.533)/(378.0266-56.533) 

	NationalLabs[line[2]].append(np.array([round(x,4)*1.6,round(y,4)]))

file1 = open("roi_33_names.txt", "r") 
NationalLabsDict = np.zeros((36,2))
counter = 0; 
for line in file1:
	line =  line.strip()
	print line
	arr = NationalLabs[line]
	print arr, line,counter
	NationalLabsDict[counter] = arr[0]*2
	counter = counter +1 

# print NationalLabsDict,"\n",counter
np.save("PosMatrix", NationalLabsDict)

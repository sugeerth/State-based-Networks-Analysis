# -*- coding:utf-8 -*-
import json
import numpy as np
from collections import defaultdict
import pprint
parsed_json = json.load(open("dblp_coauthorship1995_to_2017.json"))

all_authors= defaultdict(int) 
unique_authors = set()

for index, record in enumerate(parsed_json): 
	if (record[2] in range(2015,2018,1)): 
		all_authors[record[0]] +=1
		all_authors[record[1]] +=1  
		unique_authors.add(record[1])

k_degree_filter = 10
k_core_authors = {k: v for k, v in all_authors.iteritems() if v > k_degree_filter}

author_lookup = dict()

out = open('roi_dblp_authors.txt', 'w')
for index, author in enumerate(k_core_authors):
	author_lookup[author] = index 
	out.write(author.encode('utf8')+'\n')
out.close()

out = open('roi_dblp_year.txt', 'w')
for index in range(2010,2018,1): 
	out.write(str(index).encode('utf8')+'\n')
out.close()

time_filter = 5  

year_lookup = dict()
years = range(2015,2018,1)

for index, year in enumerate(years): 
	year_lookup[year] = index 

Author_Core = np.zeros((index+1,len(k_core_authors),len(k_core_authors)),dtype=np.float64)

pprint.pprint(k_core_authors.keys())
pprint.pprint(author_lookup)

counter = 0 
year = set() 
for index, record in enumerate(parsed_json): 
	if (record[0] in k_core_authors.keys()) and (record[1] in k_core_authors.keys()) and (record[2] in years): 
		year.add(record[2])
		counter = counter+1 
		print year_lookup[record[2]], author_lookup[record[0]],author_lookup[record[1]]
		Author_Core[year_lookup[record[2]], author_lookup[record[0]],author_lookup[record[1]]] += 1 

print counter, "Values", year

outfile = open('timeVaryingData.npy','w')
np.save(outfile, Author_Core)

nonzeroind = np.nonzero(Author_Core) 
print nonzeroind

outfile.close()
print len(k_core_authors), np.shape(Author_Core)
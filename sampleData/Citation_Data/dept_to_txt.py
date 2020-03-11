# -*- coding:utf-8 -*-
import json
import numpy as np
from collections import defaultdict
import pprint

x = []
with open("email-Eu-core-temporal-Dept3.txt") as outfile: 
	for l in outfile:
		x.append(l.strip())

print x
import json 

connection_file = open('dblp 2.json', 'r')
conn_string = json.load(connection_file)
print len(conn_string)

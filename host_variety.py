#!/usr/bin/env python


import taxonomy as tax

file_name = 'taxid10239.nbr.txt'

f = open(file_name,'r')
x=f.read()
f.close()

x = x.split('\r')
uniques = []
for entry in x[2:]:
	try:
		host = entry.split('\t')[2]
		if not host in uniques:
			uniques.append(host)
	except:
		pass
print unique



if __name__ == '__main__':


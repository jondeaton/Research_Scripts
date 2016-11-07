#!/usr/bin/env python
#This script extracts the number of sequences for each different kind of 
#phage stored in the NCBI database

def is_phage(host):
        return 'bacteria' in host or 'archaea' in host

file_name = 'taxid10239.nbr.txt'
f = open(file_name,'r')
x=f.read()
f.close()

entries = x.split('\r')
phages = {}

for entry in entries[2:-1]:
	split_entry = entry.split('\t')
	host = split_entry[2]
	name = split_entry[3]
	if is_phage(host):
		if name in phages:
			phages[name]+=1
		else:
			phages[name] = 1

write_name = 'phage_variety.txt'
f = open(write_name,'w')
f.write('Number of different phages:%d\n'%len(phages))
for phage in phages:
	f.write(phage+': %d\n'%phages[phage])
f.close()

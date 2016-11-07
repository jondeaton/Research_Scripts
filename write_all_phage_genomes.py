#!/usr/bin/env python
#This python script will find all phages and write the fasta files for them

import os
from Bio import Entrez
import time

Entrez.email = 'jdeaton@stanford.edu'
wait_time = 0.35
ascn_file_name = '/Users/jonpdeaton/Documents/research/phage_search/data/all_phage_ascessions.txt'
write_file = 'all_phage_genomes.txt'

#Extract Ascession numbers:
print 'Extracting phage ascession numbers...',
ascn_nums = []
f = open(ascn_file_name,'r')
ascn_nums = f.read().split('\n')[1:]
f.close()
print 'done'
num_phages = len(ascn_nums)

f = open(write_file,'w')
print 'Writing genomes...\n'
i = 1
for phage in ascn_nums:
	print 'Retrieving: %s (phage genome %d of %d)...'%(phage,i,num_phages), 
	try:
		f.write(Entrez.efetch(db='nucleotide', id=phage, rettype='fasta',retmode='text').read())
		print 'done. ',
	except:
		print 'ERROR. '
	i += 1
	print 'Waiting...'
	time.sleep(wait_time)

f.close()
print '\nProcess Complete.'

#!/usr/bin/env python
#This script will create a file of fasta sequences requested using Entrez efetch.
#The input should be a taxid file with in the 3rd

import os
from Bio import Entrez
import time
import argparse


Entrez.email = 'jdeaton@stanford.edu'
wait_time = 0.35

ascn_file_name = '/Users/jonpdeaton/Documents/research/phage_search/data/all_phage_ascessions.txt'
write_file = 'all_phage_genomes.txt'

if __name__ == '__main__':
    Entrez.email = 'jdeaton@stanford.edu'
    wait_tile = 0.35
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-db','--database', default='nucleotide', type=str, help='database for search')
    parser.add_argument('query',type=str,help='Entrez search query')
    parser.add_argument('-n','--num_results',type=int,default='all',help='number of search results to use')

    args = parser.parse_args()
    database = args.database
    query = args.query
    num_results = args.num_results

    results = Entrez.esearch(db=
    Entrez.efetch(db=, id=phage, rettype='fasta',retmode='text').read()
    time.sleep(wait_time)

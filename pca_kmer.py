#!/usr/bin/env python
#This script is for clustering all phage sequences found in the NCBI
#===================================================================
#OUTPUT (3 FILES)
#
#Principal component  Data file: k<>_m<>_p<>_PCA.csv

import os, sys
import numpy as np
import random

import kmeans as km
import kspace as ks
import sequences as seq
import argparse

#Returns a list of all fasta sequences within a file seperated by \n\n
def readFastaCompilationFile(file_name):
	return open(file_name).read().split("\n\n")
	
def getSeqObjs(fastas):
	return [seq.dnaSequence('phage',**{'fasta':fasta}) for fasta in fastas]

def clusterSequences(sequences, num_clusters, kmer_length):
	datapoints = []
	for sequence in sequences:
		sequence.setKspaceVector(kmer_length)
		sequence.normalizeKspaceVector()
		datapoints.append(sequence.kspaceVector)
	datapoints = np.array(datapoints)
	print '(number of points, number of dimensions): %s'%datapoints.shape.__str__()
	return km.kmeans(datapoints, num_clusters)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('kmer_length',type=int,default=3,help='Length of kmer')
	parser.add_argument('num_clusters',type=int,default=2,help='Number of clusters')
	parser.add_argument('-s','--sample',type=int,help='Number of phage to be samples from all')
	args = parser.parse_args()

	kmer_length = args.kmer_length
	num_clusters = args.num_clusters
	sample = args.sample

	data_directory = "/local10G/jdeaton/data/PCA/"

	phage_file = '/local10G/jdeaton/data/all_phage_genomes.txt'
	print 'Reading file: (%s)'
	all_phage = readFastaCompilationFile(phage_file)
	print "Read %d phage genomes from file"%len(all_phage)
	if sample:
		selected_phage = random.sample(all_phage, sample)
	else:
		sample = len(all_phage)
		selected_phage = all_phage

	print "Sampling %d of %d phage" % (sample, len(all_phage))
	phage_sequences = getSeqObjs(selected_phage)

	print 'Clutering normalized kmer-count vectors'
	clusters = clusterSequences(phage_sequences, num_clusters, kmer_length)

	print "Retrieving principal components of dataset"
	pcs = clusters.getPC(2)

	print "Writing file"
	output_file_name = "%sk%d_m%d_p%s_PCA.csv"%(data_directory, kmer_length, num_clusters, sample)
	np.savetxt(output_file_name, pcs, delimiter =',')
	print "Done"
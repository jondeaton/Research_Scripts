#!/usr/bin/env python
#KSPACE MODULE
#This file will convert a contig to "k-space" by kmers

import random
import numpy as np

#For getting the DNA sequence out of a fasta file
def fasta2seq(fasta):
	return ''.join(fasta.split('\n')[1:])

def seq2int(seq, syms):
        int_seq = ''
        for letter in seq:
                if not letter in syms:
                        int_seq += '-'
                else:
                        int_seq += str(syms.index(letter))
        return int_seq

def getRandomSeq(length, symbols):
	rndSeq = ''
	for _ in xrange(length):
		rndSeq += symbols[random.randint(0, len(symbols)-1)]
	return rndSeq

def toKspace(sequence, k, symbols, normalize=False):

	num_kmers = len(sequence) - k + 1

	if normalize:
		counter = 1 / float(num_kmers)
	else:
		counter = 1

	integer_sequence = seq2int(sequence, symbols)
	kSpaceValues = np.array([0 for _ in xrange(len(symbols)**k)])

	for i in xrange(num_kmers):
		integer_kmer = integer_sequence[i:i+k]
		if not '-' in integer_kmer:
			kSpaceValues[int(integer_kmer, len(symbols))] += counter
	
	return kSpaceValues

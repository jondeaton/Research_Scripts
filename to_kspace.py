#!/usr/bin/env python
#This file will convert a contig to "k-space" by kmers

import os, sys
import subprocess as sp

if not len(sys.argv) <4 :
	print 'Usage : kspace [ascession] [k] [symbols]'
	print ' eg: kspace FJ230960 10 nucleotide'
	exit()

ascn = str(sys.argv([1])
k = int(sys.argv[2])
syms = str(sys.argv[3])
if syms == 'nucleotide'
	syms = 'ATGC'
elif syms == 'protein'
	syms 'AGCTURYNWSMKBHDV'

def ascn_to_kspace():
	search = '$esearch -db %s -query %s'%{symbols,ascession}
	search_results = sp.check_output([search])
	fasta = sp.check_output([])
	return to_kspace(extract_fasta_seq(fasta),k, symbols)

#For getting the DNA sequence out of a fasta file
def extract_fasta_seq(fasta, symbols, no_read):
        seq = fasta.replace(' ','')
        seq = seq.replace('\n','')
        for i in range(len(seq))[::-1]:
                if not seq[i] in symbols + no_read:
                        return seq[i+1:]

def to_kspace(contig, k, syms):
	int_contig = seq_to_int(contig.upper(), syms.upper())
	kspace_values = []
	kspace_indicies = []
	for i in range(len(contig)-k+1):
		int_mer = int_contig[i:i+k]		
		if not '-' in int_mer:
			kspace_index = int(int_mer,len(syms))
			if kspace_index in kspace_indicies:
				kspace_values[kspace_indicies.index(kspace_index)]+=1
			else:
				kspace_indicies.append(kspace_index)
                        	kspace_values.append(1)

	sort(kspace_indicies, kspace_values, 0, len(kspace_values)-1)
	return [kspace_indicies, kspace_values]

def seq_to_int(seq, syms):
	int_seq = ''
	for letter in seq:
		if not letter in syms:
			int_seq += '-'
		else:
			int_seq += str(syms.index(letter))
	return int_seq

#Quick-sort algorithm by kspace index
def sort(A, B, lo, hi):
	if lo < hi:
		p = partition(A, B, lo,hi)
		sort(A, B, lo, p-1)
		sort(A, B,  p+1, hi)

def partition(A, B, lo, hi):
	pivot = A[hi]
	i = lo
	for j in range(lo, hi):
		if A[j] <= pivot:
			swap(A,i,j)
			swap(B,i,j)
			i+=1
	swap(A,i,hi)
	swap(B,i,hi)
	return i

def swap(A,i,j):
	s = A[j]
        A[j] = A[i]
        A[i] = s

print ascn_to_kspace(ascn,k,):

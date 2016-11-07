#!/usr/bin/env python
#This a module that contains functionality for kmer clustering

import numpy as np
from numpy import linalg as LA
import random as rand
import os, sys

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




def kmeans(X,k):
        n = len(X[0])
        means = init_means(X,k)
        S = assign(X,means)
        avg_mse = get_avg_mse(S)
        new_avg_mse = avg_mse*2
        while abs(new_avg_mse - avg_mse)/(avg_mse) >= 0.1:
                S = assign(X, means)
                means = get_means(S)
                avg_mse = new_avg_mse
                new_avg_mse = get_avg_mse(S)
        return S

#Selects k random and unique entries from X to use as the initial guess for means
def init_means(X, k):
        means = []
        used = []
        xi = rand.randint(0,len(X)-1)
        for i in range(k):
                while xi in used:
                        xi = rand.randint(0,len(X)-1)
                means.append(X[xi])
                used.append(xi)
        return means

#Sort X in to groups S by minimum square error from mean
def assign(X,means):
        k = len(means)
        S=[]
        for i in range(k):
                S.append([])
        for v in X:
                min_sq_er = square_error(v,means[0])
                min_index = 0
                for mi in range(1,k):
                        sq_er = square_error(v,means[mi])
                        if sq_er <= min_sq_er:
                                min_index = mi
                                min_sq_er = sq_er
                S[min_index].append(v)
        return S

def get_means(S):
        means = []
        for group in S:
                means.append(vect_mean(group))
        return means

def square_error(va,vb):
        #||va - vb||^2 = <va,va> + <vb,vb> - 2<va,vb>
        return np.dot(va,va) + np.dot(vb,vb) - 2*np.dot(va,vb)

def mean_sq_err(s):
        v_bar = vect_mean(s)
        N = len(s)
        mse = 0
        for v in s:
                mse += square_error(v_bar,v)/float(N)
        return mse

def get_avg_mse(S):
        avg_mse = 0
        r = len(S)
        for group in S:
                if not group == 0:
                        avg_mse += mean_sq_err(group)
                else:
                        r-=1
        return avg_mse/float(r)

def vect_mean(v_group):
        N = len(v_group)
        n = len(v_group[0])
        v_bar = [0]*n
        for v in v_group:
                for k in range(n):
                        v_bar[k]+= v[k]/float(N)
        return v_bar


#!/usr/bin/env python

import numpy as np
import pydendroheatmap as pdh

import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd

def kmers(k, symbols='ATGC'):
        singles = []
        for i in range(len(symbols)):
                singles.append(symbols[i])
        return extend_mers(singles, k-1, symbols)

def extend_mers(mers, k, symbols):
        if k == 0:
                return mers
        extd_mers = []
        for base in symbols:
                extension = ['']*len(mers)
                for i in range(len(mers)):
                        extension[i] = base + mers[i]
                extd_mers = extd_mers + extension
        return extend_mers(extd_mers, k-1, symbols)

def normalize_rows(X):
    for i in xrange(size(X)[0]):
        X[i][:] /= np.sum(X[i][:])
    return X

def size(array):
    shape = array.shape
    if len(shape) == 1:
        return (1, shape[0])
    else:
        return shape

def run():
    counts = 'phage_kmer_count_k4_c0_s2255.csv'
    headers = 'phage_kmer_headers_k4_c0_s2255.txt'

    data = normalize_rows(np.loadtxt(counts, delimiter=','))
    row_labels = np.array([header.split('|')[3] for header in open(headers, 'r').readlines()[1:]])
    col_labels = np.array(kmers(4))

    N = 50

    data = data[:N,:N]
    row_labels = row_labels[:N]
    col_labels = col_labels[:N]

    # cluster the rows
    row_dist = ssd.squareform(ssd.pdist(data))
    row_Z = sch.linkage(row_dist)
    row_idxing = sch.leaves_list(row_Z)

    #cluster the columns
    col_dist = ssd.squareform(ssd.pdist(data.T))
    col_Z = sch.linkage(col_dist)
    col_idxing = sch.leaves_list(col_Z)

    #make the dendrogram
    data = data[:,col_idxing][row_idxing,:]
    row_labels = list(row_labels[np.array(row_idxing)])
    col_labels = list(col_labels[np.array(col_idxing)])

    heatmap = pdh.DendroHeatMap(heat_map_data=data, left_dendrogram=row_Z, top_dendrogram=col_Z)
    heatmap.colormap = heatmap.redBlackBlue
    heatmap.row_labels = row_labels
    heatmap.col_labels = col_labels
    heatmap.title = 'Bacteirophage 4-mer hierarchical clustering'
    heatmap.export('phage_heatmap.png')
    heatmap.show()

if __name__ == '__main__':
    run()
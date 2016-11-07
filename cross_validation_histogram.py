#!/usr/bin/env python

import numpy as np
import matplotlib.pylab as plt
import sys, os
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',type=str,help='input file')
    parser.add_argument('-o','--output_file',type=str,help='histogram image name')
    parser.add_argument('-b','--bins',type=int,default=10,help='number of bins in histogram')
    parser.add_argument('-x','--x_low',type=float,help='lower bound of x on plot')
    args = parser.parse_args()

    plot_dir = "/Users/jonpdeaton/Documents/research/phage_search/plots/"
    input_file = args.input_file
    if not args.output_file:
        output_file = plot_dir+input_file.split("/")[-1].split('.')[0]+"_XV_hist.png"
    
    bins = args.bins
    x_low = args.x_low

    phage_data = np.array([float(line.split()[1]) for line in open(input_file,'r').read().split('\n')[:-1] if 'phage' in line])
    bacteria_data = np.array([float(line.split()[1]) for line in open(input_file,'r').read().split('\n')[:-1] if 'bacteria' in line])

    phage_data = phage_data[~np.isnan(phage_data)]
    bacteria_data = bacteria_data[~np.isnan(phage_data)]

    file_name = input_file.split('/')[-1]
    kmer_length = int(file_name.split('_')[0].replace('k',''))
    num_clusters = int(file_name.split('_')[1].replace('m',''))
    n_fold = int(file_name.split('_')[2].replace('fold',''))

    plt.hist(phage_data, bins, histtype='bar', color='blue',label='Phage',alpha=0.8)
    plt.hist(bacteria_data, bins, histtype='bar',color='green',label='Bacteria',alpha=0.6)
    plt.xlabel('Score: ' r'$log(p-value)$')
    plt.ylabel('Abundance (within %d samples)'%len(phage_data))
    title = '%d-Fold Cross-Validation Score Histogram for Phage Predictiction'%n_fold
    plt.title(title)
    plt.legend(loc=2)
    plt.grid()
    plt.text(-1.8, 112, 'Kmer: %dbp'%kmer_length)
    plt.text(-1.8, 103, '%d k-means clusters'%num_clusters)
    font = {'weight':'bold','size':12}
    plt.rc('font', **font)
    if x_low:
        plt.xlim([x_low,0])
    plt.savefig(output_file)
    os.system('open %s'%output_file)


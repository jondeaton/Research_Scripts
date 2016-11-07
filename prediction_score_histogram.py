#!/usr/bin/env python

import numpy as np
import matplotlib.pylab as plt
import sys, os
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',type=str,help='input file')
    parser.add_argument('-o','--output',type=str,default='histogram.png',help='histogram image name')
    parser.add_argument('-b','--bins',type=int,default=10,help='number of bins in histogram')
    parser.add_argument('-t','--title',type=str,default='Prediction algorithms score distribution',help='title for histogram plot')
    args = parser.parse_args()
    
    input_file = args.input_file
    output = args.output
    bins = args.bins
    title = args.title

    data = np.array([float(line.split()[1]) for line in open(input_file,'r').read().split('\n')[:-1]])

    data = data[~np.isnan(data)]
    
    plt.hist(data, bins, histtype='bar',alpha=0.8)
    plt.xlabel('Score')
    plt.ylabel('Abundance')
    plt.title(title)
    plt.grid()
    font = {'weight':'bold','size':12}
    plt.rc('font', **font)
    plt.savefig(output)
    os.system('open %s'%output)


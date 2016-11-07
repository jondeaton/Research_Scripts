#!/usr/bin/env python
#This file plotts a distribution of kmer abundance in phage genomes

import sys, os
import matplotlib.pyplot as plt
from math import log
import numpy as np
import argparse

def log4(x):
    #For looking on logarithmic scale
    return log(float(x)+1, 4)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dataFile', type = str, help='.csv file to be plotted')
    parser.add_argument('-b','--bins', type = int, default = 16, help='number of histogram bins')
    parser.add_argument('-x','--xlim', type = int, default = 0, help='upper limit on displayed x-axis')
    parser.add_argument('-l','--log', action = 'store_true', default = False, help='log4 of x-axis')
    
    args = parser.parse_args()
    dataFile = args.dataFile
    bins = args.bins
    x_limit = args.xlim
    
    datFileName = dataFile.split('/')[-1]
    imageDir = '/Users/jonpdeaton/Documents/research/phage_search/plots/'
    imageFile = datFileName[0:-4] + '.png'
        
    f = open(dataFile,'r')
    contents = f.read()
    f.close()
    specificPhages = contents.split('\n')[0]
    if args.log:
        kmerCounts = map(log4, contents.split('\n')[1].split(','))
    else:
        kmerCounts = map(float, contents.split('\n')[1].split(','))
    
    kmerLength = int(round(log(len(kmerCounts),4)))
    
    plt.hist(kmerCounts, bins , alpha = 0.70)
    if args.log:
        log = 'log4 '
    else:
        log = ''
    plt.xlabel(log + 'kmer frequency')
    plt.ylabel('Abundance')
    plt.title('k-mer frequency for k = %d, phage: %s'%(kmerLength, specificPhages))
    #plt.xticks(np.arange(0,300,3))
    plt.grid()
    
    if x_limit:
        plt.xlim([0, x_limit])
    
    #imageFile = 'kmerDistribution%d_%s.png'%(kmerLength, specificPhages.replace(',','_'))
    plt.savefig(imageDir+imageFile)
    #plt.show()
    os.system('open %s%s'%(imageDir, imageFile))

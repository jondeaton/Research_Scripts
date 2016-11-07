#!/usr/bin/env python
#Makes a plain histogram of a csv file

import numps as np
import matplotlib.pyplot as plt
import sys, os
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file',type=str,help='input csv file')
    parser.add_argument('-b','--bins', default = 10, type=int,help='number of bins in histogram')
    parser.add_argument('-o','--output',default='histogram.png',help='image name')
    csv_file = sys.argv[1]
    
    args = parser.parse_args()
    
    csv_file = args.csv_file
    bins = args.bins
    output = args.output
    
    contents = map(float, open(csv_file,'r').read().split(','))
    
    plt.hist(contents, bins)
    plt.grid()
    plt.savefig(output)

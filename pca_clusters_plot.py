#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import os, argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',type=str,help='PCA data file')
    parser.add_argument('-o','--output_file',type=str,help='output file')
    args = parser.parse_args()

    input_file = args.input_file
    if args.output_file:
        output_file = arg.output_file
    else:
        output_dir = '/Users/jonpdeaton/Documents/research/phage_search/plots/'
        output_file = output_dir + input_file.split('/')[-1].split('.')[0] + '.png'

    data = np.genfromtxt(input_file,delimiter=',')
    colors =['b','g','r','c','m','y','b']

    num_clusters = int(round(1 + max(data[:,0])))
    
    for cluster in xrange(num_clusters):
        plt.plot(data[data[:,0].astype(int) == cluster][:,[1,2]], 'o%s'%colors[cluster%len(colors)])
    plt.grid()

    input_file_name = input_file.split('/')[-1]
    kmer_length = int(input_file_name.split('_')[0].replace('k',''))
    num_phage = int(input_file_name.split('_')[2].replace('p',''))

    plt.title('PCA of %d-mer phage sequences'%kmer_length)
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    
    plt.savefig(output_file)
    os.system('open %s'%output_file)

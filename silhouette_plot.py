#!/usr/bin/env python
#This file reads a csv file with silhouette values and makes a plot for that

import sys, os
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    input_file = sys.argv[1]
    plot_directory = "/Users/jonpdeaton/Documents/research/phage_search/plots/"
    
    if len(sys.argv) == 3:
        output_file = sys.argv[2]
    else:
        output_file = '' + plot_directory + input_file[:-3].split('/')[-1] + '_sil.png'

    print 'Reading csv file...'
    f = open(input_file, 'r');
    s = f.read().split(',')
    f.close()
    print 'done'
    while 'nan' in s:
        s.remove('nan')
    for i in xrange(len(s)):
        s[i] = float(s[i])
    
    print 'Making .png plot image...'
    plt.clf()
    y_pos = np.arange(len(s))
    plt.barh(y_pos, s, align='center', alpha=1)
    plt.text(0,-0.1*len(s),'Average S = %.3f'%np.mean(s))
    plt.xlabel('S')
    plt.title('Silhouettes')
    plt.xlim([-1.05, 1.05])
    print 'done'
    print 'saving image file...'
    plt.savefig(output_file)
    print 'done'
    os.system('open %s'%output_file)
    #plt.show()

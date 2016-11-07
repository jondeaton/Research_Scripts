#!/usr/bin/env python
#Make a histogram of virus length

import pylab as P
import numpy as np

readFile = '/Users/jonpdeaton/Documents/research/phage_search/data/virusLengths.csv'

if __name__ == '__main__':
    
    f = open(readFile,'r')
    lengths = map(int, f.read().split(','))
    print 'Smallest phage: %d bp'%min(lengths)
    print 'Largest  phage: %d bp'%max(lengths)
    
    n, bins, patches = P.hist(lengths, 70, normed = 0, histtype = 'stepfilled')
    P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
    P.grid()
    P.xlabel('Phage Sequence Length')
    P.ylabel('Abundance')
    
    labelnums = np.arange(0,max(lengths)+1,50000)
    labels = [str(nums/1000)+'kbp' for nums in labelnums]
    P.xticks(labelnums,labels, rotation='30')
    
    P.title('Phage Sequence Length Histogram')
    font = {'weight':'bold','size':12}
    P.rc('font',**font)
    P.margins(0.2)

    P.savefig('phageLengthHist.png')

    #P.show()

#!/usr/bin/env python
#This function will recursively generate all kmers for a given d print them on to the screen

import sys
if len(sys.argv) == 1:
	print 'Usage : kmers [k] [symbols]' 
	exit()
k = int(sys.argv[1])
if k > 8:
	print "why...?"
	exit()
symbols = str(sys.argv[2])

def kmers(k, symbols):
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

print kmers(k, symbols)

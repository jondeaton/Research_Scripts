#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
import kmer
import taxonomy as tax

if __name__ == '__main__':

    phage_file = 'all_phage_genomes.fasta'
    headers, seqs = kmer.read_fasta(phage_file)
    
    i = 0
    orf_counts = []
    lengths = []
    for seq in seqs:
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write("Looking for ORFs in %d of 2255 sequences..." % (i + 1))
        sys.stdout.flush()

        orfs = tax.find_orfs(seq)
        num_orfs = len(orfs)
        orf_counts.append(num_orfs)

        lengths += [orf[1] - orf[0] for orf in orfs]
        i += 1

    print "done"
    np.savetxt('num_phage_orfs.csv', list(orf_counts), delimiter=',',fmt='%d',header='#Phage ORF counts')

    plt.subplot(1, 2, 1)
    plt.hist(orf_counts, 120, color='green', alpha=0.6, edgecolor='green')
    plt.title('Phage ORF Count Hisrogram')
    plt.ylabel('Abundance')
    plt.xlabel('ORFs in Genome')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.hist(lengths, 100, color='blue', alpha=0.6, edgecolor='blue')
    plt.title('ORF Length Historgram')
    plt.ylabel('Abundance')
    plt.xlabel('Base Pairs')
    plt.grid(True)

    plt.show()

#!/usr/bin/env python

import os

if __name__ == '__main__':

    cut = 10000
    sample = 2255
    kmer_lengths = range(1,7)
    inputs = ['/local10G/jdeaton/data/all_phage_genomes.txt', '/local10G/jdeaton/data/bacteria_genomes/','/local10G/jdeaton/data/metagenomics/super_contigs.BijahRoadSide4.fasta']

    output_stems = ['phage_kmer', 'bacteria_kmer','bijahRS4_kmer']
    ids = ['', ' -i .fna.gz', '']

    for i in xrange(len(inputs)):
        input = inputs[i]
        output_stem = output_stems[i]
        identifier = ids[i]

        for k in kmer_lengths:
            output_csv = '%s_count_k%d_c%d_s%d.csv' % (output_stem, k, cut, sample)
            header_out = '%s_headers_k%d_c%d_s%d.csv' % (output_stem, k, cut, sample)
            os.system('sbatch job_kmer_counting.sh %s %s %s %d %d %d %s' % (input, output_csv, header_out, k, sample, cut, identifier))
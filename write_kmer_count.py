#!/usr/bin/env python
#write_kmer_count.py

import sys
sys.path.append('.')
import os, argparse, timeit, random
import sequences as seq
import kspace as ks
import numpy as np

def append_kmer_data(fasta, kmer_filename, header_filename, kmer_length, cut_length, symbols):
    split_fasta = fasta.split()
    del fasta
    fasta_header = split_fasta[0]
    sequence = ''.join(split_fasta[1:])
    del split_fasta
    if not cut_length:
        uncut = True
        cut_length = len(sequence)
    else:
        uncut = False

    for cut in xrange(len(sequence)/cut_length):
        start = cut*cut_length
        end = (cut+1)*cut_length
        sub_sequence = sequence(start, end)
        kspace_vector = ks.toKspace(sub_sequence, kmer_length, symbols)
        del sub_sequence
        np.savetxt(open(kmer_filename,'ab'), kspace_vector, delimiter=',', header=head)
        del kspace_vector
        if uncut:
            header_entry = '%s base pairs %d to %d (whole sequence)\n' % (fasta_header, start+1, end+1)
        else:
            header_entry = '%s base pairs %d to %d (cut)\n' % (fasta_header, start+1, end+1)
        open(header_file,'a').write(header_entry)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input fasta compilation file OR input directory containing fasta files')
    parser.add_argument('output_csv', type=str, help='Filename for a CSV file containing kmer-count data')
    parser.add_argument('-i','--file_identifier', type=str, help='File identifier: All files in the input with file names containing this identifier will be used for kmer counting. This argument also specifies that the input is a directory containing fasta files, not a fasta compilation directory.')
    parser.add_argument('-k','--kmer_length', type=int, default=1,help='kmer length')
    parser.add_argument('-h','--header_file', type=str, default='fasta_headers', help='Filename of header file containing the fasta headers of all sequences used in kmer-counting. _k<kemr_length>_s<sample>_c<cut_length>.txt will be appended to end of this string with the appropriate parameters')
    parser.add_argument('-s','--sample', type=int, help='Randomly sample input fasta strings')
    parser.add_argument('-c','--cut', type=int, help='Randomly sample a substring of this length from all dna sequences')
    parser.add_argument('-y','--symbols', type=str, default='ATGC', help='Symbols used for kmer counting')
    args = parser.parse_args()

    input = args.input
    if not input.endswith('/'):
        input += '/'
    output_csv = args.output_csv
    file_identifier = args.file_identifier
    kmer_length = args.kmer_length
    sample = args.sample
    cut_length = args.cut_length
    header_file = '%s_k%d_s%d_c%d.txt'% (args.header_file, kmer_length, sample, cut_length)
    symbols = args.symbols


    head = 'from %s, sampled %d sequences, k-mer length: %d, cut to length: %d bp, symbols: %s)' % (input, sample, kmer_length, cut_length, symbols)

    open(output_csv,'w').write('#K-mer count data file: %s' % head)
    open(header_file,'w').write('#K-mer count fasta header file: ' % head)

    tic = timeit.default_timer()
    if file_identifier:
        #Directory containing fasta files
        selected_files = [file for file in os.listdir(input) if file_identifier in file]
        if sample:
            selected_files = random.sample(selected_files, sample)

        num_seqs = len(selected_files)
        open(output_csv,'w').write('')
        print 'Counting %d-mers in %d sequences' % (kmer_length, num_seqs)
        for i in xrange(num_seqs):
            file = selected_files[i]
            fasta = open(input+file).read()
            append_kmer_data(fasta, output_csv, header_file, kmer_length, cut_length, symbols)
            del fasta
    else:
        #Single file containing all fasta files
        selected_fastas = seq.readFastaCompilationFile(input)
        if sample:
            selected_fastas = random.sample(selected_fastas, sample)
        num_seqs = len(selected_fastas)
        print 'Counting %d-mers in %d sequences' % (kmer_length, num_seqs)
        for fasta in selected_fastas:
            append_kmer_data(fasta, output_csv, header_file, kmer_length, symbols)
        del selected_fastas

    toc = timeit.default_timer()
    print 'Elapsed time: %.3f seconds' % (toc - tic)

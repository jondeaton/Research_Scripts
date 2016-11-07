#!/usr/bin/env python

# This script prepares a contig file for input into the PHAST web-app
# This will split your file into smaller files each with less than 10Mbp total
# and will filter out sequences less than 5kbp by default

import argparse
import os, sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('-ll', '--min_len', type=int, default=5e3, help='minimum length requirement')
    parser.add_argument('-ul', '--max_len', type=int, default=1e7, help='maximum length')
    args = parser.parse_args()

    input_file = args.input
    min_len = args.min_len
    max_len = args.max_len

    print "Reading file... ",
    sys.stdout.flush()
    fastas = open(input_file, 'r').read().split('>')[1:]
    print "found: %d fasta sequences" % len(fastas)

    print "Writing files... ",
    sys.stdout.flush()

    file_num = 0
    total_length = max_len
    for fasta in fastas:

        seq_len = len(''.join(fasta.split()[1:]))

        if total_length + seq_len >= max_len:
            dot_index = input_file.index('.')
            output_file = "%s_phast_%d%s" % (input_file[:dot_index], file_num, input_file[dot_index:])
            try:
                os.system('rm %s' % output_file)
            except:
                pass
            f = open(output_file, 'wa')
            file_num += 1
            total_length = 0

        if seq_len >= min_len:
            f.write(">" + fasta)
            total_length += seq_len

    print "made %d new files" % file_num
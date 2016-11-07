#!/usr/bin/env python

# This script trims a fasta file to a new fasta file with only fasta entries that
# meet a specified length requirement

import argparse
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('output', type=str, help='Output file')
    parser.add_argument('length', type=int, help='length requirement')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    length_req = args.length

    print "Reading file... ",
    sys.stdout.flush()
    fastas = open(input_file, 'r').read().split('>')[1:]
    print "done"
    print "Found: %d fastas" % len(fastas)
    print "Finding long fastas... ",
    sys.stdout.flush()
    long_fastas = [fasta for fasta in fastas if len(''.join(fasta.split()[1:])) >= length_req]
    print "done"
    print "Found: %d fastas >%dkb" % (len(long_fastas), length_req/1000)
    print "Writing file... ",
    sys.stdout.flush()
    open(output_file,'w').write('>'.join(long_fastas))
    print "done"
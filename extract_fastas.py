#!/usr/bin/env python

# This script will write all of the fastas that contain the tag specified by the -a option to a new file
# usage: python extract_fasas.py input_file.fasta output_file.fasta -a query

import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Write fasta sequences with a certain identifier to a new file')
    parser.add_argument('input_file', type=str, help='Input fasta compilation file')
    parser.add_argument('output_file', type=str, help='Output fasta compilation file')
    parser.add_argument('-id', '--args', type=str, nargs='+')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    identifiers = args.args

    fid = open(output_file,'w')

    for fasta in open(input_file, 'r').read().split('>'):
        for id in identifiers:
            if id in fasta:
                fid.write('>'+fasta)
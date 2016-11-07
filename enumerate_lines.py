#!/usr/bin/env python

# This script will enumerate the lines of a file putting integers at the beginning of each line

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='File in which lines will be enumerated')
    parser.add_argument('-s', '--start_value', type=int, default=1, help='Number at which to begin enumeration')
    parser.add_argument('-r', '--line_skip', type=int, default=0, help='Number of lines to skip a the beginning of the file')
    parser.add_argument('-f','--format', type=str, default='%d.\t', help='Enumberation format.')
    args = parser.parse_args()

    input_file = args.input_file
    start_value = args.start_value
    line_skip = args.line_skip
    format = args.format

    lines = open(input_file,'r').readlines()
    number = start_value
    f = open(input_file,'w')

    for skipped_line in lines[:line_skip]:
        f.write(skipped_line)

    for line in lines[line_skip:]:
        f.write((format + line) % number)
        number += 1

    f.close()
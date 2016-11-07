#!/usr/bin/env python

import numpy as np
import argparse, os, random


def matrix_shape(array):
    shape = array.shape
    if len(shape) == 2:
        return shape
    else:
        return (1, shape[0])

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Input file to reduce in size')
    parser.add_argument('output_file', type=str, help='Reduced output file')
    parser.add_argument('-r', '--rows', type=int, help='Number of rows in reduced csv')
    parser.add_argument('-c', '--columns', type=int, help='Number of columns in reduced csv')
    parser.add_argument('-d','--delimiter', type=str, default=',', help='CSV delimiter')
    parser.add_argument('-s', '--skip_rows', type=int, default=0, help='Number of rows to skip')
    parser.add_argument('-f','--format', type=str, default='%d', help='Data format')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    rows = args.rows
    columns = args.columns
    delimiter = args.delimiter
    skip_rows = args.skip_rows
    format = args.format

    fid = open(input_file,'rb')
    header = ''
    for row in xrange(skip_rows):
        header += fid.readline()
    data = np.loadtxt(fid, delimiter=delimiter, skiprows=0)

    if rows:
        data = data[np.random.randint(matrix_shape(data)[0], size=rows,:]

    if columns:
        data = data[:, np.random.randint(matrix_shape(data)[1], size=columns)]

    np.savetxt(output_file, data, fmt=format, delimiter=delimiter, header=header)
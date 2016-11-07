#!/usr/bin/env python

import os
import argparse
import fileIO
import learning
import kmer
import phamer
import warnings
import logging
import numpy as np
import matplotlib
warnings.simplefilter('ignore', UserWarning)
matplotlib.use("Agg")
import matplotlib.pyplot as plt

__version__ = 1.0
__author__ = "Jonathan Deaton (jdeaton@stanford.edu)"
__license__ = "No license"

logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: fix this shit
def test_cut_response(directory, N=5, eps=[0.1, 0.1], min_pts=[2, 2], file_name='cut_response.svg', method='combo'):
    '''
    This function tests the effect of sequence cut length on Phamer learning algorithm
    :param directory: The directory that contains the k-mer count data for different sized cute
    :param N: Number of iterations of DBSCAN
    :param eps: DBSCAN distance threshold
    :param min_pts: DBSCAN minimum points per cluster
    :param filename: The filename to save the output image to
    :return: A dictionary mapping cut length to ROC AUC values
    '''
    files = [os.path.join(directory, file) for file in os.listdir(directory)]
    cuts = [2000, 5000, 7500, 10000, 100000]
    aucs = []
    for cut in cuts:
        validator = cross_validator()

        phage_file = [os.path.join(directory, file) for file in files if 'phage' in file and '_c%s_' % str(cut) in file][0]
        bacteria_file = [os.path.join(directory, file) for file in files if 'bacteria' in file and '_c%s_' % str(cut) in file][0]

        phage_kmers = kmer.read_kmer_file(phage_file, normalize=True, old=True)[1]
        bacteria_kmers = kmer.read_kmer_file(bacteria_file, normalize=True, old=True)[1]

        logger.info("Loaded k-mers from: %s and %s" % (os.path.basename(phage_file), os.path.basename(bacteria_file)))
        phage_scores, bacteria_scores = validator.cross_validate(phage_kmers, bacteria_kmers, N, eps=eps, min_pts=min_pts, method=method)
        auc = validator.predictor_performance(phage_scores, bacteria_scores)[2]
        aucs.append(auc)

    plt.figure(figsize=(9, 6))
    plt.plot(np.array([0] + cuts) / 1000.0, [0] + aucs, 'b-o')
    plt.grid(True)
    plt.xlabel('Cut Size (kbp)')
    plt.ylabel('ROC AUC')
    plt.savefig(file_name)
    return dict(zip(cuts, aucs))


if __name__ == '__main__':

    if False and args.cuts:
        # todo: fix this
        logger.info("Testing cut response... directory: %s" % args.cuts_directory)
        cut_response_output_filename = os.path.join(validator.output_directory, 'cut_response.svg')
        test_cut_response(args.cuts_directory, N=args.N_fold, method=args.method, file_name=cut_response_output_filename)
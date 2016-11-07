#!/usr/bin/evn python
'''
This script contains some random functions that I made
'''

def most_likely_prophage(sequence, phage_kmers, assignment=None):
    '''
    This function finds the 7.5kbp region of a sequence most likely to be a prophage within a sequence
    :param sequence: A string representing the DNA sequence of interest
    :param phage_kmers: A numpy array containing the k-mer counts of
    :param assignment: An optional parameter specifying a clustering assignment of the phage k-mer data-points
    :return: A tuple containing the start and stop indicies of the most likely prophage region in the sequence
    '''
    window = 7500
    slide = 100
    if len(sequence) <= window:
        return (0, len(sequence))

    if assignment is None:
        assignment = learning.dbscan(phage_kmers, 0.017571, 16, expected_noise=0.35)

    phage_centroids = learning.get_centroids(phage_kmers, assignment)
    kmer_length = int(np.log(phage_kmers.shape[1]) / np.log(4))

    num_windows = 1 + (len(sequence) - window) / slide
    slides_per_window = window / slide
    num_slides = 1 + len(sequence) // slide
    slide_kmers = np.zeros((num_slides, phage_kmers.shape[1]))
    for i in xrange(num_slides):
        slide_kmers[i] = kmer.count(sequence[slide * i:slide * (i + 1)], kmer_length, normalize=False)

    scores = np.zeros(num_windows)
    for i in xrange(num_windows):
        window_kmer_freqs = kmer.normalize_counts(np.sum(slide_kmers[i:i+slides_per_window], axis=0))
        scores[i] = learning.get_density(window_kmer_freqs, phage_centroids)
    del slide_kmers

    start = np.argmax(scores)
    stop = start + slides_per_window

    return (slide * start, slide * stop)


def find_orfs(sequence, start_codon='ATG', stop_codons=['TAA', 'TGA', 'TAG'], min_length=60, max_length=1500):
    '''
    This function finds open reading framed (ORFs) a sequence
    :param sequence: The sequence to look for ORFs in
    :param start_codon: The sequence of a start codon in a string
    :param stop_codons: A list of sequences that are stop codons
    :param min_length: The minimum length of a coding regions
    :param max_length: The maximum length of a coding region
    :return: A list of tuples containing the start and stop locations of ORFs: (start, stop)
    '''
    orfs = []
    start = -1
    while True:
        start = sequence.find(start_codon, start + 1)
        if start == -1:
            break
        stop = find_stop(sequence, start, stop_codons=stop_codons, min_length=min_length, max_length=max_length)
        if stop:
            orfs.append((start, stop + 3))
    return orfs


def find_stop(sequence, start, stop_codons=['TAA', 'TGA', 'TAG'], min_length=60, max_length=1500):
    '''
    Thus function finds the stop codon that comes after a start codon
    :param sequence: The sequence to search for the stop codon in
    :param start: The location of the start codon
    :param stop_codons: The potential stop codons to look for
    :param min_length: The minimum length of a coding regions
    :param max_length: The maximum length of a coding region
    :return: The index of the beginning of the stop codon. None will be returned if no stop codon is found
    '''
    for i in xrange(3 * (min_length // 3), max_length, 3):
        codon = sequence[start + i: start + i + 3]
        if codon in stop_codons:
            return start + i


def translate(sequence):
    '''
    This function translates a coding sequence into a amino acid sequence by a standard codon table
    :param sequence: The coding region in a string format to be translated
    :return: The amino acid sequence represented as a string
    '''
    codon_table = {
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M', 'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K', 'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L', 'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V', 'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E', 'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S', 'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
    'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_', 'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W',
    }

    sequence = sequence.upper().replace('\n', '').replace(' ', '')
    peptide = ''

    for i in xrange(len(sequence) // 3):
        peptide += codon_table[sequence[3 * i: 3 * (i + 1)]]
    return peptide

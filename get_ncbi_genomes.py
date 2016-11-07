#!/usr/bin/env python
'''
This script is for getting bacteria genomes from NCBI by navigating through the NCBI FTP database
'''
import sys
import argparse
import os
import random
from ftplib import FTP

month_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

def log_on(ftp_address, username, verbose=False):
    '''
    This function logs onto a FTP server
    :param ftp_address: Address of the server
    :param username: The username of the person
    :param verbose: Verbose output
    :return: The ftp object to navagate with
    '''
    if verbose:
        print 'Connecting to %s ...' % ftp_address,
        sys.stdout.flush()
    ftp = FTP(ftp_address)
    if verbose:
        print "done"
        print "Logging in...\t",
        sys.stdout.flush()
    text = ftp.login('anonymous', username)
    if verbose:
        print text
    return ftp

def cd(ftp, location, verbose=False):
    '''
    This function changes directory
    :param ftp: The FTP object
    :param location: The location to change directory to
    :param verbose: Verbose output
    :return: None
    '''
    if verbose:
        print 'Changing directory to %s ...\t' % location,
        sys.stdout.flush()
    text = ftp.cwd(location)
    if verbose:
        print text

def lsl(ftp, verbose=False):
    '''
    This script list all files in the current direcory with extra information
    :param ftp:The FTP object
    :param verbose:
    :return:
    '''
    if verbose:
        print "Looking up contents of %s... " % ftp.pwd(),
        sys.stdout.flush()
    files = []
    ftp.dir(files.append)
    if verbose:
        print 'found %d' % len(files)
    return files

def ls(ftp, verbose=False):
    '''
    List all files in the directory
    :param ftp: The FTP object
    :param verbose: Verbose output
    :return: A list of the files and subdirectories in the current directory
    '''
    return [file.split()[-1] for file in lsl(ftp)]

def most_recent_file(ftp):
    '''
    This function doesn't do what it purports to
    :param ftp: The FTP object
    :return:
    '''
    files = ls(ftp)
    return files[0]

def retrieve_file(ftp, file, location, verbose=False):
    '''
    This function is for retrieving a file from the server
    :param ftp: The FTP object
    :param file: The file name to retrieve from the FTP server
    :param location: The location to write it to on the local system
    :param verbose: Verbose output
    :return: None
    '''
    if verbose:
        print "Retrieving %s --> %s ..." % (os.path.basename(file), location),
        sys.stdout.flush()
    outfile = open(os.path.join(location, os.path.basename(file)), 'wb')
    text = ftp.retrbinary("RETR %s" % file, outfile.write)
    if verbose:
        print text

def get_assembly(ftp, species_directory, output_directory, verbose=False):
    extension = '.fna.gz'
    cwd = ftp.pwd()
    if verbose:
        print "Retrieving: %s..." % species_directory,
        sys.stdout.flush()
    try:
        cd(ftp, os.path.join(species_directory, 'latest_assembly_versions/'))
        latest_assembly = most_recent_file(ftp)
        cd(ftp, latest_assembly)
        assembly_files = ls(ftp)

        for file_name in assembly_files:
            if file_name in os.listdir(output_directory):
                print 'File already exists'
                return False
            elif file_name.endswith(extension) and not file_name.endswith('_cds_from_genomic.fna.gz'):
                retrieve_file(ftp, file_name, output_directory, verbose=False)
                if verbose:
                    print 'Transfer complete.'
                cd(ftp, cwd)
                return True

        if verbose:
            print 'No file found'
        cd(ftp, cwd)
        return False

    except:
        cd(ftp, cwd)
        if verbose:
            print 'Failed'
        return False

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('kingdom', type=str, help='Taxonomic Kingdom: archaea, bacteria, fungi, invertebrate, plant, protozoa, vertebrate_mammalian, vertebrate_other, other')
    parser.add_argument('output_directory', type=str, help='Directory to write retrieved files')
    parser.add_argument('-n', '--number', type=int, default=-1, help='How many to retrieve')
    parser.add_argument('-r', '--random', action='store_true', default=False, help='Flag to get random genomes')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
    args = parser.parse_args()

    kingdom = args.kingdom
    output_directory = args.output_directory
    how_many = args.number
    chose_randomly = args.random
    verbose = args.verbose

    existing_files = os.listdir(output_directory)

    ncbi_ftp = 'ftp.ncbi.nih.gov'
    ftp = log_on(ncbi_ftp, 'jdeaton@stanford.edu', verbose=verbose)

    kingdom_location = '/genomes/genbank/%s' % kingdom
    cd(ftp, kingdom_location)
    all_species = ls(ftp)

    if chose_randomly:
        random.shuffle(all_species)

    if verbose:
        print 'Retrieving new %s genomes...' % (kingdom)
    genomes_retrieved = 0
    for species_directory in all_species:
        cd(ftp, kingdom_location)
        success = get_assembly(ftp, species_directory, output_directory, verbose=verbose)
        genomes_retrieved += success
        if success and how_many != -1:
            print "%d of %d" % (genomes_retrieved, how_many)
        if genomes_retrieved == how_many:
            break
    ftp.quit()
    if verbose:
        print "Complete. Retrieved: %d" % genomes_retrieved

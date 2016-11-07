#!/usr/bin/env python
'''
This script will combine a number of GenBank files together into a single file
'''

__version__ = 1.0
__author__ = "Jonathan Deaton (jonpauldeaton@gmail.com)"
__license__ = "None"

import os
import sys
import argparse
from datetime import datetime

def now(pretty=False, date_only=False):
    '''
    This function returns a formatted time and date string
    :param pretty: Set to true to get a pretty formatting, otherwise the string will be suitable for file extensions
    :param date_only: Set to true to only get the date in the string, not the time
    :return:
    '''
    if pretty:
        return datetime.now().strftime("%A, %d. %B %Y %I:%M %p")
    else:
        if date_only:
            return datetime.now().strftime("%Y_%m_%d")
        else:
            return datetime.now().strftime("%Y_%m_%d-%H_%M")

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    Created by Trent Mick on Fri, 19 Feb 2010 (MIT)
    Taken from: http://code.activestate.com/recipes/577058/
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def generate_summary(args, line_start='', header=None, tabbed=True):
    '''
    This function makes a summary for an output file from an argparse parsed arguments object
    :param args: The parsed arguments object used to parse the arguments from the function call
    :param line_start: what each line should start with
    :param header: sometime to write on the first line
    :param tabbed: a flag to seperate field nmaes from field values
    :return: a beautiful summary
    '''

    str_rep = args.__str__()
    str_rep = str_rep.replace('Namespace(', line_start)
    str_rep = str_rep.replace(')', '')
    str_rep = str_rep.replace(', ', '\n' + line_start)
    str_rep = str_rep.replace('=', ':\t') + '\n'
    str_rep = str_rep.strip()
    str_rep = line_start + "Created:\t" + now(pretty=True) + '\n' + str_rep
    if not tabbed:
        str_rep = str_rep.replace('\t', ' ')
    if header:
        str_rep = line_start + header + '\n' + str_rep
    return str_rep

def is_gb_file(file_path):
    '''
    This funciton will determine whether a particular file is (probably) a GenBank file
    :param file_path: The path to the file
    :return: True if GenBank, False otherwise
    '''
    if not os.path.exists(file_path) or not file_path.endswith('.gb'):
        return False
    
    content = open(file_path).read().strip()
    if content == '' or not content.endswith('//'):
        print "no: %s" % os.path.basename(file_path)
        return False
    
    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-in', '--input', help='Input')
    parser.add_argument('-out', '--output', help='Output')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    input = args.input
    output = args.output
    verbose = args.verbose

    if os.path.exists(input) and os.path.isdir(input):
        gb_files = [os.path.join(input, file) for file in os.listdir(input) if is_gb_file(os.path.join(input, file))]
        print "found %d files" % len(gb_files)
        combination = ''
        for file in gb_files:
            combination += open(file, 'r').read()
        open(output, 'w').write(combination)
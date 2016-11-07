#!/user/bin/env python
#This class contains classes for sequences

import os
import kspace as ks
import numpy as np

#For getting the DNA sequence out of a fasta file
def fasta2seq(fasta):
        return ''.join(fasta.split('\n')[1:])

def getRandomSeq(length, symbols):
        rndSeq = ''
        for _ in xrange(length):
                rndSeq += symbols[random.randint(0, len(symbols)-1)]
        return rndSeq

#Returns a list of all fasta sequences within a file seperated by \n\n
def readFastaCompilationFile(file_name, sample=None):
        '''Read all of the fasta files from a file with many fastas'''
        f = open(file_name,'r')
        allFastas = f.read().split('\n\n')
        f.close()
        if not sample:
                return allFastas
        else:
                return random.sample(allFastas, int(sample))

def getFastasFromDir(directory, file_extension=None, sample=None):
        all_files = os.listdir(directory)
        if file_extension:
                selected_files = [file for file in all_files if file_extension in file]
        if sample:
                selected_files = random.sample(selected_files, sample)
        return [open(directory+file,'r').read() for file in selected_files]

def getSeqObjs(fastas, label='unknown'):
        return [seq.dnaSequence(label,**{'fasta':fasta}) for fasta in fastas]

#DNA Sequence Class
#usage: dnaSequence("my_sequence",**{"fasta",my_fasta_string})
class dnaSequence():
	def __init__(self, label, **kwargs):
		self.label = label
		self.fasta = kwargs.get('fasta')
		self.symbols = kwargs.get('symbols','ATGC')
		if self.fasta:
			fastaLines = self.fasta.split()
			self.fastaHeader = fastaLines[0]
			self.sequence = ''.join(fastaLines[1:]).upper()
			self.ascession = self.fastaHeader.split('|')[3]
			self.description = self.fastaHeader.split('|')[-1]
		else:
			self.sequence = kwargs.get('sequence')
		self.length = len(self.sequence)
		self.taxid = kwargs.get('taxid')
		self.taxonomy = kwargs.get('taxonomy')
		
	def setKspaceVector(self, kmerLength):
		self.kmerLength = kmerLength
		self.kspaceVector = ks.toKspace(self.sequence, self.kmerLength, self.symbols)
		
	def normalizeKspaceVector(self):
		self.kspaceVector = self.kspaceVector/np.linalg.norm(self.kspaceVector)
	
	def rationalizeKspaceVector(self):
		self.kspaceVector = self.kspaceVector/np.sum(self.kspaceVector)
		
	def __str__(self):
		'''String representation'''
		return '%s DNA sequence of length %d: %s, %s'%(self.label, self.length, self.ascession, self.description)

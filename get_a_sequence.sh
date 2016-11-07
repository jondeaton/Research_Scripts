#!/bin/bash
DNA_sequence=$(esearch -db nucleotide -query AF503408 | efetch -format fasta)
echo $DNA_sequence

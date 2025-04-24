# main.py
from dataStructure import compress_file
from helper_functions import *


def process_and_compare(file1, file2, base1, base2):
    print("Compressing files...")
    codebook=compress_file(file1, base1)
    compress_file(file2, base2,codebook)


    mutations = compare_compressed_bin_files_same_codebook(
    "dna1.bin", "dna2.bin", "dna1.codebook.txt"
)

    for i, a, b in mutations:
        print(f"Mutation at {i}: {a} → {b}")



process_and_compare("dna_sample1.txt", "dna_sample2.txt", "dna1", "dna2")

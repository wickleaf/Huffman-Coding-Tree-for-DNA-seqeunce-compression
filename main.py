# main.py
from dataStructure import compress_file
from helper_functions import decode_binary_file, find_mutations
import argparse
import os


def process_and_compare(file1, file2, base1, base2):
    print("\n Compressing files...")
    compress_file(file1, base1)
    compress_file(file2, base2)

    print("\n Decompressing files...")
    dna1 = decode_binary_file(base1 + ".bin", base1 + ".codebook.txt")
    dna2 = decode_binary_file(base2 + ".bin", base2 + ".codebook.txt")

    print("\n Comparing DNA sequences for mutations...")
    mutations = find_mutations(dna1, dna2)

    if not mutations:
        print("No mutations found. DNA sequences match.")
    else:
        print(f"Found {len(mutations)} mutations:")
        for pos, char1, char2 in mutations:
            print(f" - Position {pos}: {char1} -> {char2}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress, decompress and compare DNA sequences for mutations.")
    parser.add_argument("--file1", required=True, help="Path to first DNA text file")
    parser.add_argument("--file2", required=True, help="Path to second DNA text file")
    parser.add_argument("--out1", default="dna1_output", help="Base name for first file output")
    parser.add_argument("--out2", default="dna2_output", help="Base name for second file output")

    args = parser.parse_args()
    process_and_compare(args.file1, args.file2, args.out1, args.out2)

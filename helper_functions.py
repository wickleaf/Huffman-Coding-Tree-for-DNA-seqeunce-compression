def loadCodeBook(codebook_path):
    """
    Loads a Huffman codebook and returns a dictionary mapping codes to characters.

    Args:
        codebook_path (str): Path to the .codebook.txt file.

    Returns:
        dict: A dictionary where keys are Huffman codes (str) and values are characters (str).
    """
    code_to_char = {}
    with open(codebook_path, "r") as f:
        for line in f:
            char, code = line.strip().split(":")
            if char.startswith("'") or char.startswith('"'):
                char = eval(char)  # Safely convert escape sequences like '\n'
            code_to_char[code] = char
    print(code_to_char)
    return code_to_char


def bit_stream_from_file(bin_path):
    with open(bin_path, "rb") as f:
        byte_data = f.read()
        padding_length = byte_data[-1]
        bits = ''.join(f"{byte:08b}" for byte in byte_data[:-1])
        return bits[:-padding_length]

def compare_compressed_bin_files_same_codebook(bin_path_1, bin_path_2, codebook_path):
    """
    Compare two Huffman-encoded .bin DNA files using a shared codebook.

    Args:
        bin_path_1 (str): Path to first .bin file.
        bin_path_2 (str): Path to second .bin file.
        codebook_path (str): Path to shared Huffman codebook file.

    Returns:
        list: List of mutations as (position, char1, char2).
    """
    code_to_char = loadCodeBook(codebook_path)
    bits1 = bit_stream_from_file(bin_path_1)
    bits2 = bit_stream_from_file(bin_path_2)

    def decode_generator(bits):
        code = ""
        for bit in bits:
            code += bit
            if code in code_to_char:
                yield code_to_char[code]
                code = ""

    gen1 = decode_generator(bits1)
    gen2 = decode_generator(bits2)

    mutations = []
    i = 0
    try:
        while True:
            c1 = next(gen1)
            c2 = next(gen2)
            if c1 != c2:
                mutations.append((i, c1, c2))
            i += 1
    except StopIteration:
        # handle case where one file is longer than the other
        try:
            for c1 in gen1:
                mutations.append((i, c1, '-'))
                i += 1
        except StopIteration:
            pass
        try:
            for c2 in gen2:
                mutations.append((i, '-', c2))
                i += 1
        except StopIteration:
            pass

    return mutations


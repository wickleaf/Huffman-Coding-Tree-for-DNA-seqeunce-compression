def load_codebook(codebook_path):
    code_to_char = {}
    with open(codebook_path, "r") as f:
        for line in f:
            display_char, code = line.strip().split(":")
            if display_char.startswith("'") or display_char.startswith('"'):
                display_char = eval(display_char)
            code_to_char[code] = display_char
    return code_to_char


def decode_binary_file(bin_path, codebook_path):
    with open(bin_path, "rb") as f:
        byte_data = f.read()
        padding_length = byte_data[-1]
        bits = ''.join(f"{byte:08b}" for byte in byte_data[:-1])
        bits = bits[:-padding_length]

    code_to_char = load_codebook(codebook_path)
    decoded_text = []
    current_code = ""
    for bit in bits:
        current_code += bit
        if current_code in code_to_char:
            decoded_text.append(code_to_char[current_code])
            current_code = ""

    return ''.join(decoded_text)


def find_mutations(dna1, dna2):
    mutations = []
    length = min(len(dna1), len(dna2))
    for i in range(length):
        if dna1[i] != dna2[i]:
            mutations.append((i, dna1[i], dna2[i]))

    if len(dna1) != len(dna2):
        longer, shorter = (dna1, dna2) if len(dna1) > len(dna2) else (dna2, dna1)
        for i in range(length, len(longer)):
            mutations.append((i, longer[i], '-' if len(shorter) <= i else shorter[i]))

    return mutations

import heapq
from collections import Counter

def countChars(data):
    """
    Count the frequency of each character in the input data.

    Args:
        data (str): The input text.

    Returns:
        Counter: A dictionary-like object mapping each character to its frequency.
    """

    return Counter(data)

def treeBuilder(data):
    """
    Build a Huffman tree from character frequency data.

    Args:
        data (dict): A dictionary mapping characters to their frequencies.

    Returns:
        list: The root node of the Huffman tree represented as a nested list.
    """

    priorityQueue = []
    counter = 0

    for char, freq in data.items():
        priorityQueue.append([freq, counter, char])
        counter += 1

    heapq.heapify(priorityQueue)

    while len(priorityQueue) > 1:
        left = heapq.heappop(priorityQueue)
        right = heapq.heappop(priorityQueue)
        newNode = [left[0] + right[0], counter, None, left, right]
        heapq.heappush(priorityQueue, newNode)
        counter += 1

    return priorityQueue[0]

def assignCode(tree):
    """
    Traverse the Huffman tree and assign binary codes to each character.

    Args:
        tree (list): The root node of the Huffman tree.

    Returns:
        dict: A dictionary mapping characters to their corresponding Huffman codes.
    """

    codeDict = {}

    def traverse(node, code=''):
        if node[2] is None:
            traverse(node[3], code + '0')
            traverse(node[4], code + '1')
        else:
            char = node[2]
            codeDict[char] = code

    traverse(tree)
    return codeDict

def buildCodeString(codeDict, ogText):
    """
    Encode the original text using the Huffman codes.

    Args:
        codeDict (dict): A dictionary mapping characters to Huffman codes.
        ogText (str): The original input text.

    Returns:
        str: The encoded text as a string of 0s and 1s.
    """

    return ''.join(codeDict[char] for char in ogText)

def save_encoded(encoded_text, codes, out_path_base):
    """
    Save the encoded binary text and the Huffman codebook to disk.

    Args:
        encoded_text (str): The encoded text as a binary string.
        codes (dict): The Huffman codebook mapping characters to codes.
        out_path_base (str): The base path for output files (excluding extensions).

    Outputs:
        - .bin file: The binary encoded data with padding info.
        - .codebook.txt file: The character-to-code mapping.
    """
    
    padding_length = (8 - len(encoded_text) % 8)
    padded_text = encoded_text + '0' * padding_length  
    
    
    byte_array = bytearray()
    for i in range(0, len(padded_text), 8):
        byte_str = padded_text[i:i+8]
        byte = int(byte_str, 2)
        byte_array.append(byte)
    
    
    with open(out_path_base + ".bin", "wb") as f:  
        f.write(byte_array)
        f.write(padding_length.to_bytes(1, 'big'))

    with open(out_path_base + ".codebook.txt", "w") as f:
        for char, code in codes.items():
            display_char = char if char not in ['\n', '\r', '\t'] else repr(char)
            f.write(f"{display_char}:{code}\n")


def compress_file(input_path, output_path_base):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    freqs = countChars(text)
    tree = treeBuilder(freqs)
    if codes is None:
        codes = assignCode(tree)
    encoded_text = buildCodeString(codes, text)

    save_encoded(encoded_text, codes, output_path_base)
    return codes

compress_file("test2.txt", "test_output")


import heapq
from collections import Counter

def countChars(data):
    return Counter(data)

def treeBuilder(data):
    priorityQueue = []
    counter=0
    for char,freq in data.items():
        priorityQueue.append([freq,counter,char])
        counter+=1
    heapq.heapify(priorityQueue)
    while len(priorityQueue)>1:
        left = heapq.heappop(priorityQueue)
        right = heapq.heappop(priorityQueue)
        newNode = [left[0]+right[0], counter, None, left, right]
        heapq.heappush(priorityQueue, newNode)
    return priorityQueue[0]

def assignCode(tree):
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
    
def buildCodeString(codeDict,ogText):
    return ''.join(codeDict[char] for char in ogText)

def save_encoded(encoded_text, codes, out_path_base):

    # with open(out_path_base + ".bin", "w") as f:
    #     f.write(encoded_text)

    
    padding_length = (8 - len(encoded_text) % 8)
    padded_text = encoded_text + '0' * padding_length  
    
    
    byteArray = bytearray()
    for i in range(0, len(padded_text), 8):
        byteStr = padded_text[i:i+8]
        byte = int(byteStr, 2)
        byteArray.append(byte)
    
    with open(out_path_base + ".bin", "wb") as f:  
        f.write(byteArray)
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
    codes = assignCode(tree)
    encoded_text = buildCodeString(codes, text)

    save_encoded(encoded_text, codes, output_path_base)


compress_file("test2.txt", "test_output")


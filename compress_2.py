import argparse
import heapq
import json
from collections import defaultdict, Counter
from typing import Dict, Tuple

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # 存储字符
        self.freq = freq   # 存储频率
        self.left = None   # 左子节点
        self.right = None  # 右子节点

    def __lt__(self, other):
        return self.freq < other.freq

def count_transition_frequencies(input_file_path: str) -> dict:
    transition_counts = defaultdict(lambda: defaultdict(int))
    total_counts = Counter()
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        for i in range(len(text) - 1):
            current_char = text[i]
            next_char = text[i + 1]
            transition_counts[current_char][next_char] += 1
            total_counts[current_char] += 1
    
    transition_probs = {}
    for current_char, next_chars in transition_counts.items():
        transition_probs[current_char] = {}
        for next_char, count in next_chars.items():
            transition_probs[current_char][next_char] = count / total_counts[current_char]
    
    return transition_probs

def build_huffman_tree(char_probs: dict) -> HuffmanNode:
    priority_queue = [HuffmanNode(char, freq) for char, freq in char_probs.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    
    return priority_queue[0]

def generate_huffman_codes(node: HuffmanNode, current_code: str = "", code_dict: Dict[str, str] = None) -> Dict[str, str]:
    if code_dict is None:
        code_dict = {}
    if node.char is not None:
        code_dict[node.char] = current_code
    if node.left is not None:
        generate_huffman_codes(node.left, current_code + "0", code_dict)
    if node.right is not None:
        generate_huffman_codes(node.right, current_code + "1", code_dict)
    return code_dict

def encode_file(input_file_path: str, output_file_path: str, huffman_codes: Dict[str, str]) -> None:
    codes_json = json.dumps(huffman_codes)
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()
    
    encoded_text = ''
    for i in range(len(input_text) - 1):
        pair = input_text[i] + input_text[i + 1]
        encoded_text += huffman_codes.get(pair, '')
    
    encoded_bits_length = len(encoded_text)
    print("编码后的总比特数:", encoded_bits_length)

    with open(output_file_path, 'wb') as output_file:
        output_file.write(len(codes_json).to_bytes(4, byteorder='big'))
        output_file.write(encoded_bits_length.to_bytes(4, byteorder='big'))
        output_file.write(codes_json.encode("utf-8"))
        
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            if len(byte) < 8:
                byte = byte.ljust(8, '0')
            byte_array.append(int(byte, 2))
        output_file.write(byte_array)

def compress(input_file_path: str, output_file_path: str) -> None:
    transition_probs = count_transition_frequencies(input_file_path)
    
    pair_probs = {}
    for current_char, next_chars in transition_probs.items():
        for next_char, prob in next_chars.items():
            pair = current_char + next_char
            pair_probs[pair] = prob
    
    root = build_huffman_tree(pair_probs)
    
    print("Huffman Tree:")
    print_huffman_tree(root)
    
    huffman_codes = generate_huffman_codes(root)
    print("Huffman Codes:")
    for pair, code in huffman_codes.items():
        print(f"'{pair}': {code}")
    
    encode_file(input_file_path, output_file_path, huffman_codes)

def print_huffman_tree(node, level=0):
    if node is not None:
        print_huffman_tree(node.right, level + 1)
        print(' ' * 7 * level + '->', node.freq)
        print_huffman_tree(node.left, level + 1)

def main(input_file_path: str, output_file_path: str) -> None:
    compress(input_file_path, output_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path.')

    args = parser.parse_args()

    main(args.input, args.output)

import argparse
import heapq
from collections import Counter
from bitio import OutputBitStream
import json

class HuffmanNode:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def run_length_encode(text):
    if not text:
        return []
    result = []
    last_char = text[0]
    count = 1
    for char in text[1:]:
        if char == last_char:
            count += 1
        else:
            result.append((last_char, count))
            last_char = char
            count = 1
    result.append((last_char, count))  # Append the last run
    return result

def build_huffman_tree(frequencies):
    priority_queue = [HuffmanNode(symbol, freq) for symbol, freq in frequencies.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_codes(node, prefix="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if node.symbol:
        code_dict[node.symbol] = prefix
    if node.left:
        generate_codes(node.left, prefix + '0', code_dict)
    if node.right:
        generate_codes(node.right, prefix + '1', code_dict)
    return code_dict

def encode_text_to_bits(output_file_path, rle_data, codes):
    with open(output_file_path, 'wb') as f:
        bit_stream = OutputBitStream(f)
        
        # Convert the codes dictionary with tuple keys to a serializable format
        serializable_codes = {f"{k[0]}_{k[1]}": v for k, v in codes.items()}
        
        # Serialize and write the Huffman codes as JSON at the beginning of the file
        codes_json = json.dumps(serializable_codes)
        codes_bytes = codes_json.encode('utf-8')
        f.write(len(codes_bytes).to_bytes(4, 'big'))  # Write the length of the JSON data
        f.write(codes_bytes)  # Write the JSON data

        # Write the encoded data
        for char, count in rle_data:
            encoded_bits = codes[(char, count)]
            for bit in encoded_bits:
                bit_stream.write(int(bit))
        bit_stream.flush()

def compress(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    rle_data = run_length_encode(text)
    frequencies = Counter(rle_data)
    root = build_huffman_tree(frequencies)
    huffman_codes = generate_codes(root)
    
    encode_text_to_bits(output_file_path, rle_data, huffman_codes)

def main():
    parser = argparse.ArgumentParser(description='Compress text files using RLE and Huffman coding.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path.')
    args = parser.parse_args()
    compress(args.input, args.output)

if __name__ == "__main__":
    main()

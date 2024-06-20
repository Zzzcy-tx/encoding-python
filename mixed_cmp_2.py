import argparse
import heapq
import json
from collections import Counter
from bitio import OutputBitStream, InputBitStream

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
    result.append((last_char, count))
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

def encode_text_to_bits(output_file_path, rle_data, char_codes, length_codes):
    with open(output_file_path, 'wb') as f:
        bit_stream = OutputBitStream(f)
        
        # Prepare char and length codes for JSON serialization
        serializable_char_codes = {str(k): v for k, v in char_codes.items()}
        serializable_length_codes = {str(k): v for k, v in length_codes.items()}

        # Serialize codes to JSON and write them to the file
        codes_json = json.dumps({'char_codes': serializable_char_codes, 'length_codes': serializable_length_codes})
        codes_bytes = codes_json.encode('utf-8')
        f.write(len(codes_bytes).to_bytes(4, 'big'))  # Write the length of the JSON data
        f.write(codes_bytes)  # Write the JSON data
        
        # Write the encoded data
        for char, count in rle_data:
            for bit in char_codes[char]:
                bit_stream.write(int(bit))
            for bit in length_codes[count]:
                bit_stream.write(int(bit))
        bit_stream.flush()

def compress(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    rle_data = run_length_encode(text)
    char_frequencies = Counter([char for char, _ in rle_data])
    length_frequencies = Counter([count for _, count in rle_data])

    char_root = build_huffman_tree(char_frequencies)
    length_root = build_huffman_tree(length_frequencies)

    char_codes = generate_codes(char_root)
    length_codes = generate_codes(length_root)
    
    print(char_codes)
    print(length_codes)
    
    encode_text_to_bits(output_file_path, rle_data, char_codes, length_codes)

def main():
    parser = argparse.ArgumentParser(description='Compress text files using RLE and Huffman coding.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path.')
    args = parser.parse_args()
    compress(args.input, args.output)

if __name__ == "__main__":
    main()

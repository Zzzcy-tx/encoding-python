import math
import json
import argparse
from collections import Counter
from typing import Dict, List, Tuple

def count_character_frequencies(input_file_path: str) -> dict:
    frequency_dict = {}
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for char in line:
                if char in frequency_dict:
                    frequency_dict[char] += 1
                else:
                    frequency_dict[char] = 1
    return frequency_dict

def shannon_fano_recursive(symbols: List[Tuple[str, float]], prefix: str, codebook: Dict[str, str]) -> None:
    if len(symbols) == 1:
        char, _ = symbols[0]
        codebook[char] = prefix
        return

    total_prob = sum([prob for char, prob in symbols])
    cumulative_prob = 0
    split_index = 0

    for i, (char, prob) in enumerate(symbols):
        cumulative_prob += prob
        if cumulative_prob >= total_prob / 2:
            split_index = i
            break

    left_part = symbols[:split_index+1]
    right_part = symbols[split_index+1:]

    shannon_fano_recursive(left_part, prefix + '0', codebook)
    shannon_fano_recursive(right_part, prefix + '1', codebook)

def compute_shannon_fano_codes(char_freqs: Dict[str, int]) -> Dict[str, str]:
    total_chars = sum(char_freqs.values())
    probabilities = [(char, freq / total_chars) for char, freq in char_freqs.items()]
    
    # Sort characters by probability (descending order)
    probabilities.sort(key=lambda item: item[1], reverse=True)
    
    codebook = {}
    shannon_fano_recursive(probabilities, "", codebook)
    
    return codebook

def compute_expected_code_length(codes: Dict[str, str], char_freqs: Dict[str, int]) -> float:
    total_chars = sum(char_freqs.values())
    expected_length = 0
    for char, code in codes.items():
        p = char_freqs[char] / total_chars
        expected_length += p * len(code)
    return expected_length

def encode_file(input_file_path: str, output_file_path: str, codes: Dict[str, str]) -> None:
    codes_json = json.dumps(codes)
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()
    
    encoded_text = ''
    for char in input_text:
        encoded_text += codes.get(char, '')
    
    encoded_length = len(encoded_text)
    
    with open(output_file_path, 'wb') as output_file:
        output_file.write(len(codes_json).to_bytes(4, byteorder='big'))
        output_file.write(encoded_length.to_bytes(4, byteorder='big'))
        
        output_file.write(codes_json.encode("utf-8"))
        
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            if len(byte) < 8:
                byte = byte.ljust(8, '0')
            byte_array.append(int(byte, 2))
        output_file.write(byte_array)

def compress(input_file_path: str, output_file_path: str) -> None:
    character_fre_dict = count_character_frequencies(input_file_path)
    print(character_fre_dict)
    
    shannon_fano_codes = compute_shannon_fano_codes(character_fre_dict)
    print("Shannon-Fano Codes:")
    for char, code in shannon_fano_codes.items():
        print(f"'{char}': {code}")
    
    expected_length = compute_expected_code_length(shannon_fano_codes, character_fre_dict)
    print(f"Expected Shannon-Fano Code Length: {expected_length:.2f} bits per symbol")

    encode_file(input_file_path, output_file_path, shannon_fano_codes)

def main(input_file_path: str, output_file_path: str) -> None:
    compress(input_file_path, output_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path.')

    args = parser.parse_args()

    main(args.input, args.output)

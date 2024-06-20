import json
import argparse
from bitio import InputBitStream


class BitStreamReader:
    def __init__(self, file):
        self.file = file
        self.current_byte = 0
        self.bit_position = 8  # Start at 8 to trigger reading the first byte

    def read_bit(self):
        if self.bit_position == 8:
            byte = self.file.read(1)
            if not byte:
                return None  # End of file reached
            self.current_byte = byte[0]
            self.bit_position = 0

        bit = (self.current_byte >> (7 - self.bit_position)) & 1
        self.bit_position += 1
        return bit

def decode_text_from_bits(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as f:
        # Read the length of the JSON data
        length_bytes = f.read(4)
        codes_length = int.from_bytes(length_bytes, 'big')
        
        # Read the JSON data containing the Huffman codes
        codes_json_bytes = f.read(codes_length)
        codes_json = codes_json_bytes.decode('utf-8')
        codes = json.loads(codes_json)
        char_codes = {v: k for k, v in codes['char_codes'].items()}
        length_codes = {v: k for k, v in codes['length_codes'].items()}
        
        bit_reader = BitStreamReader(f)
        decoded_text = []

        while True:
            char_code = ''
            length_code = ''
            
            # Decode the character using the Huffman codes
            while char_code not in char_codes:
                bit = bit_reader.read_bit()
                if bit is None:
                    break  # End of file or stream
                char_code += str(bit)
            if char_code not in char_codes:
                break  # End of character code stream

            char = char_codes[char_code]
            
            # Decode the length using the Huffman codes
            while length_code not in length_codes:
                bit = bit_reader.read_bit()
                if bit is None:
                    break  # End of file or stream
                length_code += str(bit)
            if length_code not in length_codes:
                break  # End of length code stream

            count = int(length_codes[length_code])
            decoded_text.append(char * count)

    with open(output_file_path, 'wb') as file:
        file.write(''.join(decoded_text).encode('utf-8'))


def decompress(input_file_path, output_file_path):
    decode_text_from_bits(input_file_path, output_file_path)

def main():
    parser = argparse.ArgumentParser(description='Decompress text files using RLE and Huffman coding.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path.')
    args = parser.parse_args()
    decompress(args.input, args.output)

if __name__ == "__main__":
    main()


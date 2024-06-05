import argparse
import json
from typing import Dict

from bitio import InputBitStream


def decoding(input_file_path: str) -> Dict[int, str]:
    # 本样例代码仅给出一个例子用以说明，你需要设计自己的译码方式。
    return {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: '\n'
    }


def decode_file(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as file:
        codes_length = int.from_bytes(file.read(4), byteorder='big')    # 读取编码表长度
        encoded_length = int.from_bytes(file.read(4), byteorder='big')  # 读取有效编码长度
        # print(codes_length, encoded_length)
        codes_json = file.read(codes_length)                            # 读取编码表
        encoded_data = file.read(encoded_length)                        # 读取有效编码数据
        
        bit_string = ''.join(f'{byte:08b}' for byte in encoded_data)    # 将编码数据转换为二进制字符串

        huffman_codes = json.loads(codes_json.decode('utf-8'))          # 将编码表转换为字典
        # print(codes_json)
        decode_map = {code: char for char, code in huffman_codes.items()}# 反转霍夫曼编码表

    current_code = ""
    decoded_text = ""
    sum = 0
    for bit in bit_string:
        current_code += bit
        if sum < encoded_length:
            if current_code in decode_map:
                decoded_text += decode_map[current_code]
                current_code = ""  # 重置当前编码字符串
        sum = sum + 1
    
    with open(output_file_path, 'wb') as file:
        file.write(decoded_text.encode('utf-8'))


def decompress(input_file_path: str, output_file_path: str) -> None:
    file_header_size = 4
    char_count = 0
    bit_count = 0
    encoded_binary = 0
    decoding_map = decoding(input_file_path)
    output_file = open(output_file_path, 'w')
    with open(input_file_path, 'rb') as f:
        first_four_bytes = f.read(file_header_size)
        data_len = int.from_bytes(first_four_bytes, byteorder='big')
        input_bit_stream = InputBitStream(f)
        while True:
            bit = input_bit_stream.read()
            encoded_binary = encoded_binary << 1 | bit
            bit_count += 1
            if bit_count == 3:
                output_file.write(decoding_map[encoded_binary])
                encoded_binary = 0
                bit_count = 0
                char_count += 1
                if char_count == data_len:
                    break


# ------------------------------分割线----------------------------------
# 你可以按照需求，自由修改(增加或删减)分割线以上的所有内容。
# 分割线以下你仅可以修改main函数的具体内容，但请保证main函数的输入参数为
# ’输入文件路径‘(存储压缩后文件的路径名)和’输出文件路径‘(存储解压后文件的路径名)，两者顺序不可调换。

def main(input_file_path: str, output_file_path: str) -> None:
    decode_file(input_file_path, output_file_path)
    # decompress(input_file_path, output_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path.')

    args = parser.parse_args()

    main(args.input, args.output)

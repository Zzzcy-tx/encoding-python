import argparse
from typing import Dict

from bitio import OutputBitStream


def encoding(input_file_path: str) -> Dict[str, tuple[int, int]]:
    # 本样例代码仅给出一个例子用以说明，你需要根据原始数据文件确定你的编码方式。
    return {
        'a': (0, 3),
        'b': (1, 3),
        'c': (2, 3),
        'd': (3, 3),
        'e': (4, 3),
        'f': (5, 3),
        'g': (6, 3),
        '\n': (7, 3)
    }


def compress(input_file_path: str, output_file_path: str) -> None:
    file_header_size = 4  # bytes
    encoding_map = encoding(input_file_path)
    with open(input_file_path, 'r') as f:
        input_file_data = f.read()
    output_file = open(output_file_path, 'wb')
    output_file.write(len(input_file_data).to_bytes(file_header_size, byteorder='big'))
    bit_buffer = OutputBitStream(output_file)
    for char in input_file_data:
        code, bit_number = encoding_map[char]
        for i in range(bit_number - 1, -1, -1):
            bit_buffer.write((code >> i) & 1)
    bit_buffer.flush()
    output_file.close()


# ------------------------------分割线----------------------------------
# 你可以按照需求，自由修改(增加或删减)分割线以上的所有内容。
# 分割线以下你仅可以修改main函数的具体内容，但请保证main函数的输入为
# ’输入文件路径‘(即原始数据文件的文件路径名)和’输出文件路径‘(即存储压缩后文件的文件路径名)，两者顺序不可调换。

def main(input_file_path: str, output_file_path: str) -> None:
    compress(input_file_path, output_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path.')

    args = parser.parse_args()

    main(args.input, args.output)

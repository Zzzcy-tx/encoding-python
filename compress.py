import argparse
import heapq
import json
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

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # 存储字符
        self.freq = freq   # 存储频率
        self.left = None   # 左子节点
        self.right = None  # 右子节点

    # 定义比较操作，以便在优先队列中正确排序
    def __lt__(self, other):
        # 比较频率，以频率为优先队列的比较基准
        return self.freq < other.freq

def count_character_frequencies(input_file_path: str) -> dict:
    """
    Reads an input file and counts the frequency of each character.

    Parameters:
    input_file_path (str): The path to the input file whose characters are to be counted.

    Returns:
    dict: A dictionary where keys are characters and values are the count of each character.
    """
    frequency_dict = {}
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for char in line:
                if char in frequency_dict:
                    frequency_dict[char] += 1
                else:
                    frequency_dict[char] = 1
    return frequency_dict


def build_huffman_tree(char_freqs):
    # 创建一个优先队列，并为每个字符创建一个节点，加入到队列中
    priority_queue = [HuffmanNode(char, freq) for char, freq in char_freqs.items()]
    heapq.heapify(priority_queue)  # 将列表转换成堆

    # 当堆中只剩下一个元素时停止，那个元素就是树的根节点
    while len(priority_queue) > 1:
        # 弹出频率最小的两个节点
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        # 创建一个新节点，它的频率是两个子节点频率的和
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        # 将新节点放回堆中
        heapq.heappush(priority_queue, merged)

    # 返回堆中的最后一个元素，即霍夫曼树的根节点
    return priority_queue[0]


def print_huffman_tree(node, level=0):
    """递归打印霍夫曼树的每个节点及其频率。
    参数:
    node (HuffmanNode): 当前遍历到的节点。
    level (int): 当前节点的深度，用于格式化输出。
    """
    if node is not None:
        print_huffman_tree(node.right, level + 1)  # 先遍历右子树
        print(' ' * 7 * level + '->', node.freq)  # 打印当前节点频率
        print_huffman_tree(node.left, level + 1)  # 再遍历左子树


def generate_huffman_codes(node, current_code="", code_dict=None):
    """
    递归生成霍夫曼编码。
    参数:
    node (HuffmanNode): 当前遍历到的霍夫曼树节点。
    current_code (str): 到达当前节点的路径编码。
    code_dict (dict): 存储字符及其对应霍夫曼编码的字典。
    返回:
    dict: 字符与其对应的霍夫曼编码的字典。
    """
    if code_dict is None:
        code_dict = {}

    # 如果是叶子节点，保存该字符的编码
    if node.char is not None:
        code_dict[node.char] = current_code

    # 如果不是叶子节点，继续递归遍历
    if node.left is not None:
        generate_huffman_codes(node.left, current_code + "0", code_dict)
    if node.right is not None:
        generate_huffman_codes(node.right, current_code + "1", code_dict)

    return code_dict

import pickle

def encode_file(input_file_path, output_file_path, huffman_codes):
    # 将霍夫曼编码表转换为JSON字符串
    codes_json = json.dumps(huffman_codes)
    print('xx',codes_json)

    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()  # 读取输入文件的全部内容
        
    encoded_length = len(input_text)

    encoded_text = ''
    for char in input_text:
        encoded_text += huffman_codes.get(char, '')  # 根据霍夫曼编码表编码

    with open(output_file_path, 'wb') as output_file:
        output_file.write(len(codes_json).to_bytes(4, byteorder='big'))  # 写入编码表长度
        output_file.write(encoded_length.to_bytes(4, byteorder='big'))   # 写入有效编码长度
        print(len(codes_json),encoded_length)
        
        output_file.write(codes_json.encode("utf-8"))  # 写入编码表
        
        # 将编码数据转换为字节并写入
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            if len(byte) < 8:
                byte = byte.ljust(8, '0')
            byte_array.append(int(byte, 2))
        output_file.write(byte_array)




def compress(input_file_path: str, output_file_path: str) -> None:
    file_header_size = 4  # bytes
    encoding_map = encoding(input_file_path)
        
    character_fre_dict = count_character_frequencies(input_file_path)   # 统计字符频率
    print(count_character_frequencies(input_file_path))                 # 打印字符频率
    
    root = build_huffman_tree(character_fre_dict)           # 构建霍夫曼树
    print_huffman_tree(root)                                # 打印霍夫曼树
    
    huffman_codes = generate_huffman_codes(root)           # 生成霍夫曼编码
    print("Huffman Codes:")
    for char, code in huffman_codes.items():               # 打印霍夫曼编码
        print(f"'{char}': {code}")
    
    encode_file(input_file_path, output_file_path, huffman_codes)
    
    # with open(input_file_path, 'r') as f:
    #     input_file_data = f.read()
    # output_file = open(output_file_path, 'wb')
    # output_file.write(len(input_file_data).to_bytes(file_header_size, byteorder='big'))
    # bit_buffer = OutputBitStream(output_file)
    # for char in input_file_data:
    #     code, bit_number = encoding_map[char]
    #     for i in range(bit_number - 1, -1, -1):
    #         bit_buffer.write((code >> i) & 1)
    # bit_buffer.flush()
    # output_file.close()


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

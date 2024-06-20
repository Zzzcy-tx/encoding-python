import argparse
import math
from collections import Counter, defaultdict

def compute_transition_matrix(input_text: str) -> dict:
    transition_counts = defaultdict(lambda: defaultdict(int))
    total_counts = defaultdict(int)
    
    for i in range(len(input_text) - 1):
        current_char = input_text[i]
        next_char = input_text[i + 1]
        transition_counts[current_char][next_char] += 1
        total_counts[current_char] += 1
    
    transition_matrix = {}
    for current_char, next_chars in transition_counts.items():
        transition_matrix[current_char] = {}
        for next_char, count in next_chars.items():
            transition_matrix[current_char][next_char] = count / total_counts[current_char]
    
    return transition_matrix

def compute_conditional_entropy(transition_matrix: dict, char_frequencies: dict, total_chars: int) -> float:
    conditional_entropy = 0.0
    
    for current_char, next_chars in transition_matrix.items():
        p_current = char_frequencies[current_char] / total_chars
        for next_char, p_next in next_chars.items():
            conditional_entropy += p_current * p_next * -math.log2(p_next)
    
    return conditional_entropy

def compute_performance_limit(input_file_path: str) -> float:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    total_chars = len(text)
    
    char_frequencies = Counter(text)
    
    transition_matrix = compute_transition_matrix(text)                                                  # 概率矩阵 P(X_2|X_1)

    conditional_entropy = compute_conditional_entropy(transition_matrix, char_frequencies, total_chars)  # 条件熵 H(X_2|X_1)
    
    return conditional_entropy

def main(input_file_path):
    conditional_entropy = compute_performance_limit(input_file_path)

    print(f"22.张成亦 performance limit: {conditional_entropy:.4f} bits per symbol")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')

    args = parser.parse_args()

    main(args.input)

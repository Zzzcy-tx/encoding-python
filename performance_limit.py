import argparse


def compute_performance_limit(input_file_path: str) -> float:
    # 该样板代码只是举例说明，你需要编写代码根据输入文件自行计算该值，不可以简单的给定一个值。
    performance_limit = 1
    return performance_limit


# ------------------------------分割线----------------------------------
# 你可以按照需求，自由修改(增加或删减)分割线以上的所有内容
# 分割线以下你仅可以修改main函数的具体内容，但请保证main函数的输入为’输入文件路径名’(即原始数据文件的文件路径名)，输出为理论性能下界。

def main(input_file_path):
    res = compute_performance_limit(input_file_path)
    # 需要以如下形式将理论性能下界打印出来
    print(f"序号.姓名 performance limit: {res}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path.')

    args = parser.parse_args()

    main(args.input)
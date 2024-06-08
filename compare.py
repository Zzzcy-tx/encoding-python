import argparse



def are_files_identical(file1_path: str, file2_path: str) -> bool:
    """
    Determines whether two files are identical by comparing their contents byte by byte.

    Args:
        file1_path (str): The path to the first file.
        file2_path (str): The path to the second file.

    Returns:
        bool: True if the files are identical, False otherwise.
    """
    with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
        while True:
            byte1 = file1.read(1)
            byte2 = file2.read(1)
            if byte1 != byte2:
                return False
            if not byte1 and not byte2:
                return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--in1', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--in2', '-o', type=str, required=True, help='Output file path.')

    args = parser.parse_args()

    print(are_files_identical(args.in1, args.in2))

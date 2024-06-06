import argparse



def are_files_identical(file1_path: str, file2_path: str) -> bool:
    """
    Compares the contents of two files and determines if they are identical.

    Args:
        file1_path (str): The path to the first file to be compared.
        file2_path (str): The path to the second file to be compared.

    Returns:
        bool: True if the files are identical, False otherwise.

    Example:
        file1 = 'path/to/file1.txt'
        file2 = 'path/to/file2.txt'

        if are_files_identical(file1, file2):
            print("The files are identical.")
        else:
            print("The files are not identical.")

    Notes:
        - This function reads both files line by line, which is memory-efficient for large files compared to reading the entire file content into memory.
        - The function compares lines as-is, so differences in line endings (e.g., '\n' vs '\r\n') will result in a return value of False.
        - Ensure that the files are readable and the paths are correct to avoid exceptions.
    """
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        if len(file1.readlines()) != len(file2.readlines()):
            return False
        for line1, line2 in zip(file1, file2):
            if line1 != line2:
                return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--in1', '-i', type=str, required=True, help='Input file path.')
    parser.add_argument('--in2', '-o', type=str, required=True, help='Output file path.')

    args = parser.parse_args()

    print(are_files_identical(args.in1, args.in2))

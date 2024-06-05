from io import BytesIO


class BitStreamBase:
    INIT_BIT_MASK = 0b10000000


class OutputBitStream(BitStreamBase):
    """
    Write bits to a binary file.

    Examples:
        # Example usage:
        with open("output.bin", "wb") as file:
            bit_stream = OutputBitStream(file)
            bit_stream.write_bits(1)
            bit_stream.write_bits(0)
            bit_stream.write_bits(1)
            # Continue writing other bits...
            bit_stream.flush()  # Don't forget to flush at the end to write remaining bits to the file.
    """

    def __init__(self, output_file):
        """
        Initialize the OutputBitStream instance.

        Args:
            output_file (file object): A file object used for writing bytes.

        Raise:
            TypeError: If the output_file is not a BytesIO object or a file object opened in 'wb' mode.
        """
        self._buffer = bytearray(1)
        self._bit_mask = self.INIT_BIT_MASK
        if isinstance(output_file, BytesIO) or output_file.mode == 'wb':
            self._output_file = output_file
        else:
            raise TypeError

    def write(self, bit):
        """
        Write a single bit to the _buffer and then write it to the file when the _buffer is full (8 bits).

        Args:
           bit (int): The bit to write (0 or 1).

        Raises:
           ValueError: If the input bit is not 0 or 1.
        """
        if bit != 0 and bit != 1:
            raise ValueError("Input value must be 0 or 1!")
        bit_mask = self._bit_mask
        if bit:
            self._buffer[0] |= bit_mask
        bit_mask >>= 1
        if bit_mask == 0:
            self._output_file.write(self._buffer)
            self._buffer = bytearray(1)
            self._bit_mask = OutputBitStream.INIT_BIT_MASK
        else:
            self._bit_mask = bit_mask

    def flush(self):
        """
        Flush the remaining bits (is not full of 8 bits) in the _buffer to the binary file.
        """
        if self._bit_mask != 0:
            self._output_file.write(self._buffer)
            self._buffer = bytearray(1)
            self._bit_mask = OutputBitStream.INIT_BIT_MASK


class InputBitStream(BitStreamBase):
    """
    Read a stream of bits from a binary file.

    Examples:
        # Example usage:
        with open("input.bin", "rb") as file:
            bit_stream = InputBitStream(file)
            bit = bit_stream.read()
            while bit is not None:
                # Process bit
                bit = bit_stream.read()
    """

    def __init__(self, input_file):
        """
        Initializes the InputBitStream instance.

        Args:
            input_file (file object): The input file object.

        Raises:
            TypeError: If the input_file_path is not a BytesIO object or a file object opened in 'rb' mode.
            EOFError:  If the file is empty.
        """
        if isinstance(input_file, BytesIO) or input_file.mode == 'rb':
            self._input_file = input_file
        else:
            raise TypeError
        self._buffer = input_file.read(1)
        if not self._buffer:
            raise EOFError('The file is empty.')
        self._bit_mask = self.INIT_BIT_MASK

    def read(self):
        """
        Reads the next bit from the binary file.

        Returns:
            int: The next bit read from the file (0 or 1)
        """
        bit_mask = self._bit_mask
        bit = 0 if self._buffer[0] & bit_mask == 0 else 1
        bit_mask >>= 1
        if bit_mask == 0:
            self._buffer = self._input_file.read(1)
            self._bit_mask = self.INIT_BIT_MASK
        else:
            self._bit_mask = bit_mask
        return bit

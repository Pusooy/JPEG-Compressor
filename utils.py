"""Defines some helper functions for JPEG compression."""
import os
import time

ZIGZAG_ORDER = [(0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (0, 2), (0, 3), (1, 2),
                (2, 1), (3, 0), (4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0, 5),
                (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (6, 0), (5, 1), (4, 2),
                (3, 3), (2, 4), (1, 5), (0, 6), (0, 7), (1, 6), (2, 5), (3, 4),
                (4, 3), (5, 2), (6, 1), (7, 0), (7, 1), (6, 2), (5, 3), (4, 4),
                (3, 5), (2, 6), (1, 7), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3),
                (7, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (4, 7), (5, 6),
                (6, 5), (7, 4), (7, 5), (6, 6), (5, 7), (6, 7), (7, 6), (7, 7)]


def getFileInfo(path):
    FileInfo = ''
    FileInfo += '文件路径：\n' + path + '\n\n'
    FileInfo += '文件大小： ' + str(get_FileSize(path)) + 'MB' + '\n'
    FileInfo += '创建时间：' + get_FileCreateTime(path) + '\n'
    FileInfo += '修改时间：' + get_FileModifyTime(path)
    return FileInfo


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


def get_FileAccessTime(filePath):
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


def get_huffman_table_bit_string(huffman_table):
    """Returns the huffman table bit string suitable for a jpeg file."""
    table_string = ''
    length_counts = []

    # Create array of 16
    for count in range(16):
        length_counts.append(0)

    # Figure out how many code of each length there is
    for symbol, code in huffman_table.items():
        code_length = len(code) - 1
        length_counts[code_length] += 1

    # Write that info to the string bound for the actual file
    for count in length_counts:
        table_string += (bin(count)[2:]).zfill(8)
    codes_by_code_length = []

    # Create array of size 16, each spot containing a list of codes for that length
    for count in range(16):
        codes_by_code_length.append([])

    # Figure out how many codes of each length there is
    inverse_map = {}
    for symbol, code in huffman_table.items():
        code_length = len(code) - 1
        codes_by_code_length[code_length].append(code)
        inverse_map[code] = symbol

    # Sort them
    for codes in codes_by_code_length:
        codes.sort()

    # JPEG wants the symbols stored, sorted by their code. I think this implies
    # that it wants short code lengths to long code lengths, and within each length
    # it should be sorted
    for codes in codes_by_code_length:
        for code in codes:
            table_string += (bin(inverse_map[code])[2:]).zfill(8)
    return table_string


def get_magnitude_dc(value):
    """Returns the 1 byte magnitude for a DC pixel."""
    if value < 1:
        value *= -1
    length = 0
    while value:
        value >>= 1
        length += 1
    return length


def get_ones_complement_bit_string(value):
    """Returns the ones complement bit string of a value."""
    if value == 0:
        return ''
    negative = False
    if value < 0:
        negative = True
        value *= -1
    bit_string = bin(value)[2:]  # Chop off the '0b' bin returns
    if negative:
        bit_list = list(bit_string)
        for index, bit in enumerate(bit_list):
            if bit == '0':
                bit_list[index] = '1'
            else:
                bit_list[index] = '0'
        bit_string = ''.join(bit_list)
    return bit_string

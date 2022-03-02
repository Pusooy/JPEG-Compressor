"""Implements the JPEG compression algorithm."""
import numpy

from huffmanTables import JPEG_HUFFMAN_DC_LUM, JPEG_HUFFMAN_AC_LUM
from utils import ZIGZAG_ORDER
from utils import get_magnitude_dc, get_ones_complement_bit_string

# Set numpy printing options to print floats reasonably
numpy.set_printoptions(precision=2, suppress=True)

# 亮度量化矩阵
L_QUANTIZATION_TABLE = numpy.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                    [12, 12, 14, 19, 26, 58, 60, 55],
                                    [14, 13, 16, 24, 40, 57, 69, 56],
                                    [14, 17, 22, 29, 51, 87, 80, 62],
                                    [18, 22, 37, 56, 68, 109, 103, 77],
                                    [24, 35, 55, 64, 81, 104, 113, 92],
                                    [49, 64, 78, 87, 103, 121, 120, 101],
                                    [72, 92, 95, 98, 112, 100, 103, 99]])
# 色度量化矩阵
C_QUANTIZATION_TABLE = numpy.array([[17, 18, 24, 47, 99, 99, 99, 99],
                                    [18, 21, 26, 66, 99, 99, 99, 99],
                                    [24, 26, 56, 99, 99, 99, 99, 99],
                                    [47, 66, 99, 99, 99, 99, 99, 99],
                                    [99, 99, 99, 99, 99, 99, 99, 99],
                                    [99, 99, 99, 99, 99, 99, 99, 99],
                                    [99, 99, 99, 99, 99, 99, 99, 99],
                                    [99, 99, 99, 99, 99, 99, 99, 99]])

# 初始化用于DCT变换的矩阵 ref: https://blog.csdn.net/ahafg/article/details/48808443
DCT_TABLE = numpy.array([[0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35],
                         [0.49, 0.42, 0.28, 0.1, -0.1, -0.28, -0.42, -0.49],
                         [0.46, 0.19, -0.19, -0.46, -0.46, -0.19, 0.19, 0.46],
                         [0.42, -0.1, -0.49, -0.28, 0.28, 0.49, 0.1, -0.42],
                         [0.35, -0.35, -0.35, 0.35, 0.35, -0.35, -0.35, 0.35],
                         [0.28, -0.49, 0.1, 0.42, -0.42, -0.1, 0.49, -0.28],
                         [0.19, -0.46, 0.46, -0.19, -0.19, 0.46, -0.46, 0.19],
                         [0., -0.28, 0.42, -0.49, 0.49, -0.42, 0.28, -0.1]])


def scale_quant_tables(scale_factor, l_quant_tables, c_quant_tables):
    if scale_factor <= 0:
        scale_factor = 1
    if scale_factor >= 100:
        scale_factor = 99

    for i in range(64):
        tmp = int((l_quant_tables[int(i / 8)][i % 8] * scale_factor + 50) / 100)
        if tmp <= 0:
            tmp = 1
        elif tmp > 255:
            tmp = 255
        l_quant_tables[int(i / 8)][i % 8] = tmp

        tmp = int((c_quant_tables[int(i / 8)][i % 8] * scale_factor + 50) / 100)
        if tmp <= 0:
            tmp = 1
        elif tmp > 255:
            tmp = 255
        c_quant_tables[int(i / 8)][i % 8] = tmp

    return [l_quant_tables, c_quant_tables]


def take_dct_of_component(component):
    """Selects which DCT to use (mine or scipy's FCT)."""
    for index, matrix in enumerate(component):
        # 分两步进行，因为是二维离散变换
        res = numpy.dot(DCT_TABLE, matrix)
        component[index] = numpy.dot(res, numpy.transpose(DCT_TABLE))
        # 运用这个库函数进行dct变换会更快
        # component[index] = scipy.fftpack.dct(scipy.fftpack.dct(matrix.T, norm='ortho').T, norm='ortho')


def quantize_component(component, quantization_table):
    """Quantizes a whole color component (this should be a list matrices)."""
    for index, matrix in enumerate(component):
        component[index] = matrix / quantization_table


def encode_dc(component):
    """Perform differential pulse-code modulation on the DC coefficients."""
    for index, matrix in reversed(list(enumerate(component))):
        if index == 0:
            continue  # Don't subtract the first DC term
        component[index][0][0] = matrix[0][0] - component[index - 1][0][0]


def zigzag_all(interleaved):
    """Zigzag all of the blocks (creating a list of lists)."""
    zigzaged_lists = []
    for matrix in interleaved:
        zigzaged_matrix = []
        for index in ZIGZAG_ORDER:
            zigzaged_matrix.append(matrix[index[0]][index[1]])
        zigzaged_lists.append(zigzaged_matrix)
    return zigzaged_lists


def run_length_encode(serial_list):
    """Perform run length encoding on a serialized block."""
    serial_index = 0
    run_length = []
    while serial_index < 64:
        if serial_index == 0:
            value = serial_list[serial_index]
            run_length.append((get_magnitude_dc(value),
                               get_ones_complement_bit_string(value)))
            serial_index += 1
            continue
        zero_count = 0
        while serial_index < 64 and serial_list[serial_index] == 0:
            zero_count += 1
            serial_index += 1
        if serial_index == 64:  # Rest of the block is zero
            run_length.append((0x00, ''))
            break
        while zero_count > 15:  # Encode as 16 zeroes as needed till nonzero
            run_length.append((0xF0, ''))
            zero_count -= 16
        nonzero_value = serial_list[serial_index]
        zero_count <<= 4
        zrl = zero_count | get_magnitude_dc(nonzero_value)
        run_length.append((zrl,
                           get_ones_complement_bit_string(nonzero_value)))
        serial_index += 1
    return run_length


def huffman_encode(run_length):
    """Replace the symbols with their appropriate huffman code."""
    for index, tup in enumerate(run_length):
        # Just using the luminance tables for simplicity
        if index == 0:
            tup = run_length[index]
            run_length[index] = (JPEG_HUFFMAN_DC_LUM[tup[0]], tup[1])
        else:
            tup = run_length[index]
            run_length[index] = (JPEG_HUFFMAN_AC_LUM[tup[0]], tup[1])


def dump_scan_to_string(run_lengthed_lists):
    """Dump the whole scan into a 'binary' string."""
    scan_string = ''
    for run_length in run_lengthed_lists:
        for mag, literal in run_length:
            scan_string += mag + literal
    return scan_string

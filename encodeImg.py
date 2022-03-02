"""Implements the JPEG compression algorithm."""
import numpy
import scipy.fftpack
from huffman import JPEG_HUFFMAN_DC_LUM, JPEG_HUFFMAN_AC_LUM
from imageinput import create_matrices_pixel_sequence
from imageinput import get_image, crop_image_to_multiple_eight
from imageinput import get_ycbcr_bands, get_pixels
from utils import ZIGZAG_ORDER, get_huffman_table_bit_string
from utils import get_magnitude_dc, get_ones_complement_bit_string

# Set numpy printing options to print floats reasonably
numpy.set_printoptions(precision=2, suppress=True)

# Currently just using one quantization table for the whole file
L_QUANTIZATION_TABLE = numpy.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                    [12, 12, 14, 19, 26, 58, 60, 55],
                                    [14, 13, 16, 24, 40, 57, 69, 56],
                                    [14, 17, 22, 29, 51, 87, 80, 62],
                                    [18, 22, 37, 56, 68, 109, 103, 77],
                                    [24, 35, 55, 64, 81, 104, 113, 92],
                                    [49, 64, 78, 87, 103, 121, 120, 101],
                                    [72, 92, 95, 98, 112, 100, 103, 99]])


def _take_dct_of_component(component):
    """Selects which DCT to use (mine or scipy's FCT)."""
    for index, matrix in enumerate(component):
        component[index] = scipy.fftpack.dct(scipy.fftpack.dct(matrix.T, norm='ortho')
                                             .T, norm='ortho')


def _quantize_component(component, quantization_table):
    """Quantizes a whole color component (this should be a list matrices)."""
    for index, matrix in enumerate(component):
        component[index] = matrix / quantization_table


def _encode_dc(component):
    """Perform differential pulse-code modulation on the DC coefficients."""
    for index, matrix in reversed(list(enumerate(component))):
        if index == 0:
            continue  # Don't subtract the first DC term
        component[index][0][0] = matrix[0][0] - component[index - 1][0][0]


def _zigzag_all(interleaved):
    """Zigzag all of the blocks (creating a list of lists)."""
    zigzaged_lists = []
    for matrix in interleaved:
        zigzaged_matrix = []
        for index in ZIGZAG_ORDER:
            zigzaged_matrix.append(matrix[index[0]][index[1]])
        zigzaged_lists.append(zigzaged_matrix)
    return zigzaged_lists


def _run_length_encode(serial_list):
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


def _huffman_encode(run_length):
    """Replace the symbols with their appropriate huffman code."""
    for index, tup in enumerate(run_length):
        # Just using the luminance tables for simplicity
        if index == 0:
            tup = run_length[index]
            run_length[index] = (JPEG_HUFFMAN_DC_LUM[tup[0]], tup[1])
        else:
            tup = run_length[index]
            run_length[index] = (JPEG_HUFFMAN_AC_LUM[tup[0]], tup[1])


def _dump_scan_to_string(run_lengthed_lists):
    """Dump the whole scan into a 'binary' string."""
    scan_string = ''
    for run_length in run_lengthed_lists:
        for mag, literal in run_length:
            scan_string += mag + literal
    return scan_string


from PyQt5.QtCore import QThread, pyqtSignal


class Processthread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Processthread, self).__init__()

    def run(self):
        None

    def jpeg_encode(self, input_path, quality, output_path):
        """Implements JPEG compression."""
        # Adjust quantization table
        self._signal.emit('质量因子：' + str(quality) + '%' + '\n')
        self._signal.emit('根据质量因子调整量化表' + '\n')
        scaled_quant_table = L_QUANTIZATION_TABLE
        # 根据压缩质量重新计算量化表
        scale_factor = quality
        if quality <= 0:
            scale_factor = 1
        if quality > 100:
            scale_factor = 99
        # if quality < 50:
        #     scale_factor = 5000 / quality
        # else:
        #     scale_factor = 200 - quality*2

        for i in range(64):
            tmp = int((scaled_quant_table[int(i / 8)][i % 8] * scale_factor + 50) / 100)
            if tmp <= 0:
                tmp = 1
            elif tmp > 255:
                tmp = 255
            scaled_quant_table[int(i / 8)][i % 8] = tmp

        # Display new quantization table to be used
        print('New quantization matrix after scaling:')
        print(scaled_quant_table)

        # Extract the data into pixel matrices of the Y, Cb, Cr components
        self._signal.emit('读取图像数据' + '\n')
        original = get_image(input_path)
        crop = crop_image_to_multiple_eight(original)
        width, height = crop.size

        self._signal.emit('宽：' + str(width) + 'px' + '   高：' + str(height) + 'px' + '\n')
        self._signal.emit('分离YCrCb通道' + '\n')
        lum, chromb, chromr = get_ycbcr_bands(crop)
        lum_matrices = create_matrices_pixel_sequence(get_pixels(lum),
                                                      width, height)
        chromb_matrices = create_matrices_pixel_sequence(get_pixels(chromb),
                                                         width, height)
        chromr_matrices = create_matrices_pixel_sequence(get_pixels(chromr),
                                                         width, height)

        self._signal.emit('将值域从(0,255)调整至(-127,128)' + '\n')
        # BYTE是无符号 而UV是 - 127到128
        # Shift them to be centered around 0
        all_matrices = [lum_matrices, chromb_matrices, chromr_matrices]
        for matrices in all_matrices:
            for matrix in matrices:
                matrix -= 128

        self._signal.emit('进行DCT变换' + '\n')
        # Take DCT of all
        for matrices in all_matrices:
            _take_dct_of_component(matrices)

        self._signal.emit('量化' + '\n')
        # Quantize all
        for matrices in all_matrices:
            _quantize_component(matrices, scaled_quant_table)

        self._signal.emit('取整' + '\n')
        # Round (just cast everything to an integer, this doesn't have to be exact)
        for matrices in all_matrices:
            for index, matrix in enumerate(matrices):
                matrices[index] = matrix.astype(numpy.int32)

        self._signal.emit('差分脉冲编码调制(DPCM)编码' + '\n')
        # Subtract DC components
        for matrices in all_matrices:
            _encode_dc(matrices)

        # Interleave the components
        length_of_components = len(all_matrices[0])
        interleaved = []
        for index in range(length_of_components):
            interleaved.append(all_matrices[0][index])  # Append the Y component
            interleaved.append(all_matrices[1][index])  # Append the Cb component
            interleaved.append(all_matrices[2][index])  # Append the Cr component

        self._signal.emit('Z字形编码' + '\n')
        # Zigzag all into a list of lists (each list is the zigzag of a block)
        zigzaged_lists = _zigzag_all(interleaved)

        self._signal.emit('行程长度编码(RLE)' + '\n')
        # Run length encode all
        run_lengthed_lists = []
        for serial_list in zigzaged_lists:
            run_lengthed_lists.append(_run_length_encode(serial_list))

        self._signal.emit('哈夫曼编码(熵编码)' + '\n')
        # Huffman encode the whole scan
        for run_length in run_lengthed_lists:
            _huffman_encode(run_length)

        self._signal.emit('写入JPEG文件头' + '\n')
        # Format file, add DQT, DHT, and scan
        file_string = bin(0xFFD8)[2:].zfill(16)  # SOI

        file_string += bin(0xFFE0)[2:].zfill(16)  # APP0
        file_string += bin(0x0010)[2:].zfill(16)  # Length of APP0, including the length (16 bytes)
        file_string += bin(0x4A46494600)[2:].zfill(40)  # 'JFIF\0'
        file_string += bin(0x0102)[2:].zfill(16)  # JFIF version 1.02
        file_string += bin(0x01)[2:].zfill(8)  # Units (DPI)
        file_string += bin(0x0040)[2:].zfill(16)  # Arbitrary X DPI
        file_string += bin(0x0040)[2:].zfill(16)  # Arbitrary Y DPI
        file_string += bin(0x00)[2:].zfill(8)  # X thumbnail length
        file_string += bin(0x00)[2:].zfill(8)  # Y thumbnail length

        self._signal.emit('写入量化表' + '\n')
        # Encode the quantization table
        dqt = []
        for index in ZIGZAG_ORDER:
            dqt.append(scaled_quant_table[index[0]][index[1]])
        file_string += bin(0xFFDB)[2:].zfill(16)  # DQT Marker
        file_string += bin(0x0043)[2:].zfill(16)  # Length (67), including the length bytes
        file_string += bin(0x00)[2:].zfill(8)  # Table value sizes and table identifier 0
        for value in dqt:
            file_string += (bin(value)[2:]).zfill(8)  # Add each table value

        self._signal.emit('写入哈夫曼表' + '\n')
        # Encode the huffman table
        file_string += bin(0xFFC4)[2:].zfill(16)  # DHT MARKER

        # Create bitstring representation for the huffman tables
        dc_table_string = bin(0x00)[2:].zfill(8)  # DC table, identifier 0
        dc_table = get_huffman_table_bit_string(JPEG_HUFFMAN_DC_LUM)
        ac_table_string = bin(0x10)[2:].zfill(8)  # AC table, identifier 0
        ac_table = get_huffman_table_bit_string(JPEG_HUFFMAN_AC_LUM)

        # Write the length of the huffman tables plus the 2 bytes of the length bytes
        length = int(((len(dc_table) + len(ac_table)) / 8)) + 2 + 2
        dc_table_string += dc_table
        ac_table_string += ac_table
        file_string += (bin(length)[2:]).zfill(16)

        # Write the huffman tables
        file_string += dc_table_string + ac_table_string

        self._signal.emit('写入帧图像' + '\n')
        # Start of frame
        file_string += bin(0xFFC0)[2:].zfill(16)  # SOF0 marker
        file_string += bin(0x0011)[2:].zfill(16)  # Length
        file_string += bin(0x08)[2:].zfill(8)  # Sample precision (8 bits)
        file_string += (bin(height)[2:]).zfill(16)  # 2 bytes for height
        file_string += (bin(width)[2:]).zfill(16)  # 2 bytes for width
        file_string += (bin(0x03)[2:]).zfill(8)  # Number of components
        # Y component for SOF
        file_string += bin(0x01)[2:].zfill(8)  # 1 is the Y indicator for JFIF files
        file_string += bin(0x11)[2:].zfill(8)  # Sampling frequency of 1 to 1
        file_string += bin(0x00)[2:].zfill(8)  # Quantization table identifier
        # Cb component for SOF
        file_string += bin(0x02)[2:].zfill(8)  # 2 is the Cb indicator for JFIF files
        file_string += bin(0x11)[2:].zfill(8)  # Sampling frequency of 1 to 1
        file_string += bin(0x00)[2:].zfill(8)  # Quantization table identifier
        # Cr component for SOF
        file_string += bin(0x03)[2:].zfill(8)  # 3 is the Cb indicator for JFIF files
        file_string += bin(0x11)[2:].zfill(8)  # Sampling frequency of 1 to 1
        file_string += bin(0x00)[2:].zfill(8)  # Quantization table identifier

        # Scan
        file_string += bin(0xFFDA)[2:].zfill(16)  # Scan component
        file_string += bin(0x000C)[2:].zfill(16)  # Length
        file_string += bin(0x03)[2:].zfill(8)  # Component count
        file_string += bin(0x01)[2:].zfill(8)  # Y component
        file_string += bin(0x00)[2:].zfill(8)  # DC and AC huffman table identifiers
        file_string += bin(0x02)[2:].zfill(8)  # Cb component
        file_string += bin(0x00)[2:].zfill(8)  # DC and AC huffman table identifiers
        file_string += bin(0x03)[2:].zfill(8)  # Cr component
        file_string += bin(0x00)[2:].zfill(8)  # DC and AC huffman table identifiers
        file_string += bin(0x00)[2:].zfill(8)  # Spectral selection start
        file_string += bin(0x3F)[2:].zfill(8)  # Spectral selection end (63)
        file_string += bin(0x00)[2:].zfill(8)  # Successive approximation

        # Dump the scan data
        scan_string = _dump_scan_to_string(run_lengthed_lists)

        # Add throw away bits to make it end on a byte
        if len(scan_string) % 8:
            for bit in range(8 - len(scan_string) % 8):
                scan_string += '1'

        # Zero pad any 0xFF bytes
        bytez = [scan_string[index:index + 8] for
                 index in range(0, len(scan_string), 8)]
        for index, byte in enumerate(bytez):
            if byte == '11111111':
                bytez[index] = '1111111100000000'

        # Add to file string
        file_string += ''.join(bytez)

        self._signal.emit('写入JPEG尾' + '\n')
        # EOI
        file_string += bin(0xFFD9)[2:].zfill(16)

        # Split our massive and inefficient bitstring into bytes
        bytez = [file_string[index:index + 8] for
                 index in range(0, len(file_string), 8)]
        bytez = [int(byte, 2) for byte in bytez]

        self._signal.emit('生成文件' + '\n')
        # Write all the bytes to a file
        with open(output_path, 'wb') as filepointer:
            filepointer.write(bytes(bytez))

    def encodeimg(self, inputfile, outputfile, quality):
        """Gets the options for converting a PNG to a JPEG."""
        self._signal.emit('.....开始压缩..... \n')
        import time
        import os
        start_time = time.time()
        self.jpeg_encode(inputfile, quality, outputfile)
        end_time = time.time()
        self._signal.emit('.....完成压缩..... \n\n')
        original_size = os.path.getsize(inputfile)
        new_size = os.path.getsize(outputfile)
        percent_smaller = 100 * float(original_size - new_size) / original_size

        self._signal.emit('原始图像大小: {} bytes'.format(original_size) + '\n')
        self._signal.emit('生成图像大小: {} bytes'.format(new_size) + '\n')
        self._signal.emit('压缩耗时: {:.2f} 秒'.format(end_time - start_time) + '\n')
        self._signal.emit('压缩率：{:.2f}%'.format(percent_smaller) + '\n')

        self.quit()

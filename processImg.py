import numpy
from PyQt5.QtCore import QThread, pyqtSignal

from compressAlgorithm import *
from inputImg import *
from utils import get_huffman_table_bit_string


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
        # 根据压缩质量重新计算量化表
        # 为什么这里重新定义一遍呢，因为未知原因如果不重新定义的话量化矩阵初始值将会变为上一次放缩后的值
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
        scaled_l_quant_table, scaled_c_quant_table = scale_quant_tables(quality, L_QUANTIZATION_TABLE,
                                                                        C_QUANTIZATION_TABLE)
        # 输出调整后的量化表
        str_l_table = ''
        str_c_table = ''
        for x in range(8):
            for y in range(8):
                if y == 0:
                    str_l_table += '[ '
                    str_c_table += '[ '
                str_l_table += str(scaled_l_quant_table[x][y]) + ' '
                str_c_table += str(scaled_c_quant_table[x][y]) + ' '
                if y == 7:
                    str_l_table += ']'
                    str_c_table += ']'
            str_l_table += '\n'
            str_c_table += '\n'
        self._signal.emit('调整后的亮度量化表：')
        self._signal.emit(str_l_table)
        self._signal.emit('调整后的色度量化表：')
        self._signal.emit(str_c_table)

        # Extract the data into pixel matrices of the Y, Cb, Cr components
        self._signal.emit('读取图像数据' + '\n')
        original = get_image(input_path)
        # 从左上角截去一段像素，使得宽高都能整除8
        crop = crop_image_to_multiple_eight(original)
        width, height = crop.size
        self._signal.emit('宽：' + str(width) + 'px' + '   高：' + str(height) + 'px' + '\n')

        self._signal.emit('分离YCrCb通道' + '\n')
        # 将三个通道分分离， 然后每个通道再从上至下， 从左至右 分割成诺干个 MCU（MCU大小由最高采样系数决定），
        lum, chromb, chromr = get_ycbcr_bands(crop)
        # 下面的函数将决定 MCU 块的大小，与采样系数有关
        lum_matrices = create_matrices_pixel_sequence(get_pixels(lum), width, height)
        chromb_matrices = create_matrices_pixel_sequence(get_pixels(chromb), width, height)
        chromr_matrices = create_matrices_pixel_sequence(get_pixels(chromr), width, height)

        self._signal.emit('将值域从(0,255)调整至(-127,128)' + '\n')
        # BYTE是无符号字节 RGB是0到255储存， 而YUV是- 127到128 因此这里需要处理
        # Shift them to be centered around 0
        for matrix in lum_matrices:
            matrix -= 128
        for matrix in chromb_matrices:
            matrix -= 128
        for matrix in chromr_matrices:
            matrix -= 128

        self._signal.emit('进行DCT变换' + '\n')
        # Take DCT of all
        take_dct_of_component(lum_matrices)
        take_dct_of_component(chromb_matrices)
        take_dct_of_component(chromr_matrices)

        self._signal.emit('进行量化取整' + '\n')
        # Quantize all
        quantize_component(lum_matrices, scaled_l_quant_table)
        quantize_component(chromb_matrices, scaled_c_quant_table)
        quantize_component(chromr_matrices, scaled_c_quant_table)

        # Round (just cast everything to an integer, this doesn't have to be exact)
        for index, matrix in enumerate(lum_matrices):
            lum_matrices[index] = matrix.astype(numpy.int32)
        for index, matrix in enumerate(chromb_matrices):
            chromb_matrices[index] = matrix.astype(numpy.int32)
        for index, matrix in enumerate(chromr_matrices):
            chromr_matrices[index] = matrix.astype(numpy.int32)

        self._signal.emit('差分脉冲编码调制(DPCM)' + '\n')
        # 第一个数值为DC直流分量，对直流分量采用DPCM编码，因为该值通常较大，而相邻的8x8图像数据之间的差值变化不大。
        # 所谓DCPM编码，听起来高大上，实际就是将每一个（第一个除外）MCU的直流分量（对应MCU矩阵左上角的值）都减去上一个MCU的直流分量的值
        # 这样可以增加数据中0的数目，从而更好的压缩
        # Subtract DC components
        encode_dc(lum_matrices)
        encode_dc(chromb_matrices)
        encode_dc(chromr_matrices)

        # 按照JPEG格式要求排列YCbCr通道顺序，接下来编码
        # Interleave the components
        length_of_components = len(lum_matrices)  # 8x8 DataUnit的数目
        interleaved = []
        for index in range(length_of_components):
            interleaved.append(lum_matrices[index])  # Append the Y component
            interleaved.append(chromb_matrices[index])  # Append the Cb component
            interleaved.append(chromr_matrices[index])  # Append the Cr component

        self._signal.emit('Zigzag编码' + '\n')
        # 就是从对每个MCU单元以左上角开始以 z 字型展开成一维列表
        # 返回的是一个数组， 数组元素是展开成 一维列表的 MCU 单元
        # Zigzag all into a list of lists (each list is the zigzag of a block)
        zigzaged_lists = zigzag_all(interleaved)

        self._signal.emit('行程长度编码(RLE)' + '\n')
        # Run length encode all
        run_lengthed_lists = []
        for serial_list in zigzaged_lists:
            run_lengthed_lists.append(run_length_encode(serial_list))

        self._signal.emit('哈夫曼编码(熵编码)' + '\n')
        # Huffman encode the whole scan
        for run_length in run_lengthed_lists:
            huffman_encode(run_length)

        self._signal.emit('写入SOI文件头' + '\n')
        # Format file, add DQT, DHT, and scan

        # SOI文件头 JPEG文件的开始2个字节都是FF D8这是JPEG协议规定的
        file_string = bin(0xFFD8)[2:].zfill(16)  # SOI

        self._signal.emit('写入APP0图像识别信息' + '\n')
        # APP0图像识别信息
        file_string += bin(0xFFE0)[2:].zfill(16)  # APP0
        file_string += bin(0x0010)[2:].zfill(16)  # Length of APP0, including the length (16 bytes)
        file_string += bin(0x4A46494600)[2:].zfill(40)  # 'JFIF\0'
        file_string += bin(0x0102)[2:].zfill(16)  # JFIF version 1.02
        file_string += bin(0x01)[2:].zfill(8)  # Units (DPI) 单位密度
        file_string += bin(0x0040)[2:].zfill(16)  # Arbitrary X DPI  水平像素密度
        file_string += bin(0x0040)[2:].zfill(16)  # Arbitrary Y DPI 垂直像素密度
        file_string += bin(0x00)[2:].zfill(8)  # X thumbnail length 缩略图X像素
        file_string += bin(0x00)[2:].zfill(8)  # Y thumbnail length 缩略图Y像素

        self._signal.emit('写入DQT定义量化表' + '\n')
        # Encode the quantization table
        lqt = []
        for index in ZIGZAG_ORDER:
            lqt.append(scaled_l_quant_table[index[0]][index[1]])
        cqt = []
        for index in ZIGZAG_ORDER:
            cqt.append(scaled_c_quant_table[index[0]][index[1]])
        file_string += bin(0xFFDB)[2:].zfill(16)  # DQT Marker 段标识类型
        file_string += bin(0x0084)[2:].zfill(16)  # Length (132), including the length bytes
        # 写入亮度量化表
        file_string += bin(0x00)[2:].zfill(8)  # Table value sizes and table identifier 0
        for value in lqt:
            file_string += (bin(value)[2:]).zfill(8)  # Add each table value
        # 写入色度量化表
        file_string += bin(0x01)[2:].zfill(8)  # Table value sizes and table identifier 0
        for value in cqt:
            file_string += (bin(value)[2:]).zfill(8)  # Add each table value

        self._signal.emit('写入DHT定义huffman表' + '\n')
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

        self._signal.emit('写入SOF0图像基本信息' + '\n')
        # Start of frame
        file_string += bin(0xFFC0)[2:].zfill(16)  # SOF0 marker
        file_string += bin(0x0011)[2:].zfill(16)  # Length
        file_string += bin(0x08)[2:].zfill(8)  # Sample precision (8 bits)
        file_string += (bin(height)[2:]).zfill(16)  # 2 bytes for height
        file_string += (bin(width)[2:]).zfill(16)  # 2 bytes for width
        file_string += (bin(0x03)[2:]).zfill(8)  # Number of components
        # Y component for SOF
        file_string += bin(0x01)[2:].zfill(8)  # 1 is the Y indicator for JFIF files
        # 采样系数是实际采样方式与最高采样系数之比，而最高采样系数一般＝0.5（分数表示为1 /
        # 2）。比如说，垂直采样系数＝2，那么2×0.5＝1，表示实际采样方式是每个点采一个样，也就是逐点采样；如果垂直采样系数＝1，那么：1×0.5＝0.5（分数表示为1 / 2），表示每２个点采一个样
        file_string += bin(0x11)[2:].zfill(8)  # Sampling frequency of 1 to 1
        file_string += bin(0x00)[2:].zfill(8)  # Quantization table identifier
        # Cb component for SOF
        file_string += bin(0x02)[2:].zfill(8)  # 2 is the Cb indicator for JFIF files
        file_string += bin(0x11)[2:].zfill(8)  # Sampling frequency of 1 to 1
        file_string += bin(0x01)[2:].zfill(8)  # Quantization table identifier
        # Cr component for SOF
        file_string += bin(0x03)[2:].zfill(8)  # 3 is the Cb indicator for JFIF files
        file_string += bin(0x11)[2:].zfill(8)  # Sampling frequency of 1 to 1
        file_string += bin(0x01)[2:].zfill(8)  # Quantization table identifier

        self._signal.emit('写入SOS扫描行' + '\n')
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
        scan_string = dump_scan_to_string(run_lengthed_lists)

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

        self._signal.emit('写入EOI文件尾' + '\n')
        # EOI
        file_string += bin(0xFFD9)[2:].zfill(16)

        # Split our massive and inefficient bitstring into bytes
        bytez = [file_string[index:index + 8] for
                 index in range(0, len(file_string), 8)]
        bytez = [int(byte, 2) for byte in bytez]

        self._signal.emit('生成JPEG文件' + '\n')
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

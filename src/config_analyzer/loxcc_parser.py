#!/usr/bin/env python
# -*- coding: utf-8 -*-
# implemented by Markus Fritze (https://gist.github.com/sarnau/e14ff9fe081611782a3f3cb2e2c2bacd)

import struct
import zlib
import lz4.frame
import lz4.block

LOXCC_MAGIC = 0xAABBCCEE
LZ4_MAGIC = 0x184D2204


def uncompress_loxcc(file, dest_file=None):
    if dest_file is None:
        dest_file = file.replace('LoxCC', 'Loxone')

    with open(file, "rb") as f:
        header, = struct.unpack('<L', f.read(4))
        if header == 0xaabbccee:  # magic word to detect a compressed file
            compressed_size, header3, header4, = struct.unpack('<LLL', f.read(12))
            # header3 is roughly the length of the uncompressed data, but it is a bit higher
            # header4 could be a checksum, I don't know
            data = f.read(compressed_size)
            index = 0
            result_str = b''
            while index < len(data):
                # the first byte contains the number of bytes to copy in the upper
                # nibble. If this nibble is 15, then another byte follows with
                # the remainder of bytes to copy. (Comment: it might be possible that
                # it follows the same scheme as below, which means: if more than
                # 255+15 bytes need to be copied, another 0xff byte follows and so on)
                byte, = struct.unpack('<B', data[index:index + 1])
                index += 1
                copy_bytes = byte >> 4
                byte &= 0xf
                if copy_bytes == 15:
                    copy_bytes += data[index]       # !! ord(data[index])
                    index += 1
                if copy_bytes > 0:
                    result_str += data[index:index + copy_bytes]
                    index += copy_bytes
                if index >= len(data):
                    break
                # Reference to data which already was copied into the result.
                # bytes_back is the offset from the end of the string
                bytes_back, = struct.unpack('<H', data[index:index + 2])
                index += 2
                # the number of bytes to be transferred is at least 4 plus the lower
                # nibble of the package header.
                bytes_back_copied = 4 + byte
                if byte == 15:
                    # if the header was 15, then more than 19 bytes need to be copied.
                    while True:
                        val, = struct.unpack('<B', data[index:index + 1])
                        bytes_back_copied += val
                        index += 1
                        if val != 0xff:
                            break
                # Duplicating the last byte in the buffer multiple times is possible,
                # so we need to account for that.
                while bytes_back_copied > 0:
                    if -bytes_back + 1 == 0:
                        result_str += result_str[-bytes_back:]
                    else:
                        result_str += result_str[-bytes_back:-bytes_back + 1]
                    bytes_back_copied -= 1

            if dest_file is not None:
                with open(dest_file, 'wb') as out_f:
                    out_f.write(result_str)

            return result_str


def decompress_loxcc(file):
    """
    LoxCC format [MAGIC][compressed size][uncompressed size]
     MAGIC = 0xaabbccee
    :param file:
    :return:
    """

    # uncompress_loxcc(file)

    with open(file, "rb") as f:
    # with lz4.frame.open(file,lz4.frame.)
        header, = struct.unpack('<L', f.read(4))
        compressed_size, uncompress_size, crc, = struct.unpack('<LLL', f.read(12))
        compressed_data = f.read()
        my_crc = zlib.crc32(compressed_data)

        compressed_data = b'\x04\x22\x4d\x18\x60\x6f\x73\xd8\x1a\x01\x00' + compressed_data
        # compressed_data = b'\x04\x22\x4d\x18\x60\x70\x73\x2d\xad\x02\x00' + compressed_data
        # data = lz4.frame.decompress(compressed_data)
        d_ctx = lz4.frame.create_decompression_context()
        # data, bytes_read, is_eof = lz4.frame.decompress_chunk(d_ctx, compressed_data)
        data = lz4.block.decompress(compressed_data, uncompressed_size=2048)
        a = 5

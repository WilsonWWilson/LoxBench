import os
import lzf  # TODO maybe use pythons integrated lzma module
import math
import shutil
from struct import unpack_from
from collections import namedtuple
from colorama import Fore

BLOCK_SIZE = 512
LIVE_IMG_MAGIC = 0xC2C101AC

MAGIC1 = 0x9181A2B3
MAGIC2 = 0x9181A2B4     # probably empty file
Header = namedtuple('Header', ['magic', 'block_count', 'version', 'checksum', 'compressed_size', 'raw_size', 'tmp'])

# update file contains multiple binary/update files


def unpack(file, dest_dir=None):
    """
    UPD file starts with a header of 7 UINTS: magic, size (how many sectors)
    version, checksum, compressed_size, expanded_size, tmp
    the first part is the Miniserver update image
    """
    if dest_dir is None:
        dest_dir = os.path.abspath(os.curdir).replace("src", "out")
    prepare_output_directory(dest_dir)

    files = []
    pos = 0
    try:
        print("Unpacking " + os.path.basename(file))
        with open(file, "rb") as f:
            file_size = os.path.getsize(file)
            header_size = 4 * 7
            raw = f.read(header_size)
            magic, size, *header = unpack_from("I" * 7, raw)     # size is the number of blocks and NOT bytes!
            header = Header._make(unpack_from("I" * 7, raw))
            if magic == LIVE_IMG_MAGIC:  # extract mini server data
                f.seek(BLOCK_SIZE)  # skip remaining part of sector
                if not check_checksum(f, header.checksum, header.compressed_size):
                    return
                ms_data = extract_miniserver_image(f, header)
                files.append(ms_data)
                compr_str = f'/ compressed: {sizeof_fmt(header.compressed_size)}' if header.compressed_size else ''
                print(f"extracting {ms_data[0]}\t ({sizeof_fmt(len(ms_data[1]))}{compr_str})")

                # jump to start of first file after the ms image
                pos = (size + 1) * BLOCK_SIZE
                f.seek(pos)
            else:
                print("len? {} vs {}".format(magic, file_size))

            # extract files
            while pos < file_size:
                file_data = extract_file(f)
                files.append(file_data)
                pos = int(4 * math.ceil(f.tell()/4))  # round to multiple of 4 for padding
                f.seek(pos)
    except Exception as e:
        print(f"Couldn't read file: {e}")

    write_files(dest_dir, files)
    # TODO return tree of extracted files - possibly with notes on type, etc.
    return os.path.join(dest_dir, ms_data[0])


def prepare_output_directory(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    else:
        os.mkdir(path)


def check_checksum(f, checksum, compr_size):
    pos = f.tell()
    data = f.read(compr_size)
    # the checksum is a trivial little endian XOR32 over the data
    xor_value = 0x00000000
    aligned_firmware_data = data + b'\0\0\0'  # make sure the data allows 4-byte aligned access for the checksum
    for offset in range(0, len(data), 4):
        xor_value ^= unpack_from("<L", aligned_firmware_data, offset)[0]
    f.seek(pos)
    is_valid = xor_value == checksum
    if not is_valid:
        print(f"Firmware Checksum WRONG:\t{checksum:#08x} != {xor_value:#08x}")
    return is_valid


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G']:
        if abs(num) < 1024.0:
            # return "%3.1f%s%s" % (num, unit, suffix)
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num} bytes'  # no fitting suffix? print bytes as is


def extract_miniserver_image(f, header):
    raw = f.read(header.compressed_size)
    data = lzf.decompress(raw, header.raw_size) if header.raw_size > 0 else None
    return "{:08d}_LoxLIVE.bin".format(header.version), data, header.compressed_size


def extract_file(f):
    header_size = 3 * 4
    raw = f.read(header_size)
    magic, size, compressed_size = unpack_from("I" * 3, raw)

    if magic != MAGIC1 and magic != MAGIC2:
        print("couldn't find magic number")
        raise ValueError

    pos = f.tell()
    raw = f.read(128)  # read a chunk to get the name
    name = get_zero_terminated_str(raw)
    f.seek(pos + len(name) + 1)  # go to the beginning of the file

    if compressed_size > 0:  # data is compressed
        raw = f.read(compressed_size)  # read the content of the file
        try:
            data = lzf.decompress(raw, size) if size > 0 else None
        except Exception as e:
            print(f"Couldn't decrompress '{name}': {e}")
            data = []
    else:
        data = f.read(size)

    # print status
    compr_str = f'/ compressed: {sizeof_fmt(compressed_size)}' if compressed_size else ''
    col = Fore.RED if magic == MAGIC2 else Fore.CYAN if len(data) == 0 else Fore.RESET  # MAGIC2 = empty file
    print(f"{col}extracting {name}\t ({sizeof_fmt(len(data))}{ compr_str})")   # .format(name, len(data) if data is not None else '-',

    return name, data, compressed_size


def get_zero_terminated_str(raw):
    letters = bytearray()
    for byte in raw:
        if byte == 0x00:
            break
        letters.append(byte)
    return str(letters, "latin-1")


def write_files(out_path, files):
    for name, data, _ in files:
        path = os.path.join(out_path, *name.split("/"))

        is_dir = "." not in os.path.basename(path)   # no file ext. in path
        dir_name = path if is_dir else os.path.dirname(path)
        os.makedirs(dir_name, exist_ok=True)

        if is_dir:  # nothing to write, if it's just a directory
            continue

        if data is None:   # if there is no data, just create file
            with open(path, 'a'):
                os.utime(path, None)
        else:
            with open(path, "wb") as f:
                f.write(data)


def write_file(out_path, name, data):
    path = os.path.join(out_path, *name.split("/"))

    is_dir = "." not in os.path.basename(path)   # no file ext. in path
    if is_dir:  # nothing to write, if it's just a directory
        return

    dir_name = path if is_dir else os.path.dirname(path)
    os.makedirs(dir_name, exist_ok=True)

    print("Creating '{}'".format(name))
    if data is None:   # if there is no data, just create file
        with open(path, 'a'):
            os.utime(path, None)
    else:
        with open(path, "wb") as f:
            f.write(data)

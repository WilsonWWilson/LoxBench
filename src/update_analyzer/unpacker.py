import os
import lzf  # TODO maybe use pythons integrated lzma module
import math
import shutil
from struct import unpack_from

BLOCK_SIZE = 512
LIVE_IMG_MAGIC = 0xC2C101AC

MAGIC1 = 0x9181A2B3
MAGIC2 = 0x9181A2B4     # probably empty file


def unpack(file, dest_dir=None):
    """
    UPD file starts with a header of 7 UINTS: magic, size (how many sectors)
    version, checksum, compressed_size, expanded_size, tmp
    the first part is the Miniserver update image
    """
    if dest_dir is None:
        out_path = os.path.abspath(os.curdir).replace("src", "out")
    prepare_output_directory(out_path)

    files = []
    pos = 0
    try:
        print("Unpacking " + os.path.basename(file))
        with open(file, "rb") as f:
            file_size = os.path.getsize(file)
            header_size = 4 * 7
            raw = f.read(header_size)
            magic, size, *header = unpack_from("I" * 7, raw)     # size is the number of blocks and NOT bytes!
            print("First magic: {:02X}/ size: {}".format(magic, size))
            if magic == LIVE_IMG_MAGIC:  # extract mini server data
                f.seek(BLOCK_SIZE)  # skip remaining part of sector
                print("MS: size:{} vs file_size: {}".format(size, file_size))
                ms_data = extract_miniserver_image(f, *header)
                files.append(ms_data)

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
        print("Couldn't read file: " + str(e))
        # return

    write_files(out_path, files)


def prepare_output_directory(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    else:
        os.mkdir(path)


def extract_miniserver_image(f, version, crc, compr_size, raw_size, tmp):
    raw = f.read(compr_size)
    data = lzf.decompress(raw, raw_size) if raw_size > 0 else None
    return "{:08d}_LIVE.bin".format(version), data


def extract_file(f):
    header_size = 3 * 4
    raw = f.read(header_size)
    magic, size, filesize_c = unpack_from("I" * 3, raw)

    # if magic != MAGIC1 and magic != MAGIC2:
    #     print("couldn't find magic number")
    #     raise ValueError

    pos = f.tell()
    raw = f.read(128)  # read a chunk to get the name
    name = get_zero_terminated_str(raw)

    print("'{}' -> File magic: {:02X}/ size: {:.2f}kb/ filesize: {:.2f}kb".format(name, magic, size/1024, filesize_c/1024))

    f.seek(pos + len(name) + 1)  # go to the beginning of the file
    raw = f.read(filesize_c)  # read the content of the file
    data = lzf.decompress(raw, size) if size > 0 else None

    return name, data


def get_zero_terminated_str(raw):
    letters = bytearray()
    for byte in raw:
        if byte == 0x00:
            break
        letters.append(byte)
    return str(letters, "latin-1")


def write_files(out_path, files):
    for name, data in files:
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

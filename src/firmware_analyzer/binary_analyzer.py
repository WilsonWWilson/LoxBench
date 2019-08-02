import string
import re
from .unpacker import unpack

MAGIC_DICT = {
    b'\xac\x01\xc1\xc2': 'LoxLIVE',
    b'\x1f\x8b\x08': "gz",
    b'\x42\x5a\x68': "bz2",
    b'\x50\x4b\x03\x04': "zip"
}

# drop vertical tab and form feed as those are not actually used printable characters
ASCII_CHARS = string.printable.replace('\f', '').replace(chr(11), '')


def analyze(file):
    # decompress update file first if necessary
    if file.endswith('.upd') and is_compressed(file):
        file = unpack(file, dest_dir=file.replace('.upd', '_unpacked'))

    strings = list(get_strings(file, filter_patterns=[r'_Z(\w|\d)']))
    with open(file.replace('.bin', '_filtered.txt'), 'w') as f_out:
        for s in strings:
            f_out.write(f'{s}\n')

    # TODO group strings (by build class names? maybe use get some kind of discriminator between classfiles?


def is_compressed(file):
    with open(file, 'rb') as f:
        data = f.read(12)  # read first n bytes as length of magic number may vary
        for m, name in MAGIC_DICT.items():  # compare magic numbers with variable length
            if data[:len(m)] == m:
                return m, name
    return False


def get_strings(file, min_str_len=3, filter_patterns=[], drop_duplicates=True):
    # min length of 2 yields too many false positives; lower min. once a better plausibility check is in place
    seen = set()

    with open(file, 'rb') as f:
        result = ""
        for c in f.read():
            if chr(c) in ASCII_CHARS:
                result += chr(c)    # keep building the string
                continue
            result = result.strip()
            if len(result) >= min_str_len:
                # crude plausibility check on short strings
                if len(result) > 3 or result[1] not in string.whitespace:
                    # use conditional deduplication
                    is_valid = result not in seen if drop_duplicates else True
                    # discard result if filtered pattern matches?
                    for pattern in filter_patterns:
                        if re.search(pattern, result):
                            is_valid = False
                            break
                    if is_valid:
                        yield result
            result = ""
        if len(result) >= min_str_len:  # catch result at EOF
            yield result

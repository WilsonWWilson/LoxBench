import argparse
import requests
import os
import datetime
import xml.etree.ElementTree as ET
import binascii
import logging


interested_components = [
    {'name': 'LoxConfig', 'tag': '', 'in_dir': True},
    {'name': 'WebInterface', 'attributes': ["Name='{name}'"], 'in_dir': True},
    {'name': 'LoxLIVE', 'attributes': ["Name='{name}'"], 'in_dir': True},
    {'name': 'AirBase', 'attributes': ["Name='{name}'"], 'in_dir': True},
]


def get_updatecheck():
    url = r'http://update.loxone.com/updatecheck.xml'

    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        raise ConnectionError("Could not download updatecheck.xml")


def save_updatecheck(content, archive_dir):
    os.makedirs(archive_dir, exist_ok=True)
    dt = datetime.datetime.now()
    path = os.path.join(archive_dir, "updatecheck_" + dt.strftime("%Y-%m-%d") + ".xml")
    with open(path, 'w') as f:
        f.write(content)


def updatecheck_has_changed(updatecheck, archive_dir):
    files = [f for f in os.listdir(archive_dir) if os.path.isfile(os.path.join(archive_dir, f))]
    if len(files) == 0:     # no existing files means it definitely contains new information
        return True
    last_updatecheck = sorted(files, reverse=True)[0]
    last_path = os.path.join(archive_dir, last_updatecheck)
    with open(last_path, 'r') as last_f:
        last_updatecheck = last_f.read()
        if updatecheck != last_updatecheck:
            return True
    return False


def download_interesting_binaries(content, archive_dir):
    # tag and attribute keys are used to filter the interesting entries
    # if no 'dir' is specified, the value of the Name-attribute is used as directory, unless 'save-dir'=False
    logger = logging.getLogger(__name__)

    uc = ET.fromstring(content)

    for entry in interested_components:
        extra = ''
        if 'attributes' in entry:
            extra = '[@{}]'.format(entry['attributes'][0].format(**entry))
        tag = entry.get('tag', 'update')
        pattern = './{}{}/Test'.format(tag, extra) if tag else 'Test'     # special handling for direct child-nodes of root elements
        el = uc.find(pattern)

        e = {**entry, **el.attrib}     # merge entry used to find the element and element attributes, so no information is lost
        dl_dir = os.path.join(archive_dir, e['name']) if e.get('in_dir', False) else archive_dir
        file_name = os.path.basename(e['Path'])
        if not os.path.isfile(os.path.join(dl_dir, file_name)):
            logger.info("\tDownloading " + file_name)
            content = download_binary(e['Path'])

            if 'crc32' in e:
                my_crc32 = binascii.crc32(content)
                lx_crc32 = int(e['crc32'], 16)
                if my_crc32 != lx_crc32:
                    logger.warning('CRC32 mismatch for file {}: got {} -- updatcheck.xml said: {}'.format(file_name, my_crc32, lx_crc32))

            save_file(dl_dir, file_name, content)
            logger.info("\t{} downloaded!".format(file_name))
        else:
            logger.debug("No new version of {} available".format(file_name))


def download_binary(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    else:
        raise ConnectionError("Could not download updatecheck.xml")


def save_file(dest_dir, file_name, content):
    os.makedirs(dest_dir, exist_ok=True)
    with open(os.path.join(dest_dir, file_name), 'wb') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--archive-dir", default="data", help="Directory where the downloaded files will be stored")
    parser.add_argument("-b", "--binaries-dir", default="files", help="Name of the folder in the archive where binaries will be placed")
    parser.add_argument("-u", "--updatecheck-dir", default="UpdateCheck", help="Name of the folder in the archive where updatecheck.xml-files will be placed")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.info("---- checking for updates ----")
    try:
        root_dir = args.archive_dir
        content = get_updatecheck()
        updatecheck_dir = os.path.join(root_dir, args.updatecheck_dir)
        os.makedirs(updatecheck_dir, exist_ok=True)
        if updatecheck_has_changed(content, updatecheck_dir):
            logger.info("\tUpdatecheck.xml has changed, checking available binaries")
            save_updatecheck(content, updatecheck_dir)
            bin_dir = os.path.join(root_dir, args.binaries_dir)
            os.makedirs(bin_dir, exist_ok=True)
            download_interesting_binaries(content, bin_dir)
        else:
            logger.info("\tUpdatecheck.xml hasn't changed! No action taken!")
    except Exception as exc:
        logger.error('Failed: ' + str(exc))


if __name__ == "__main__":
    FORMAT = '[%(asctime)-15s]<%(levelname)s>: %(message)s'
    # logging.basicConfig(format=FORMAT, datefmt='%Y.%d.%m %H:%M:%S', filename='LxWard.log', level=logging.INFO)
    logging.basicConfig(format=FORMAT, datefmt='%Y.%d.%m %H:%M:%S', level=logging.DEBUG)
    main()

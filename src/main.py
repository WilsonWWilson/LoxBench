from comm import LoxComm
from secrets.credentials import user, password
from api import ALL_COMMANDS
from secrets.credentials import user, password
from update_analyzer import unpacker
from config_analyzer.loxcc_parser import uncompress_loxcc#, decompress_loxcc
import asyncio
import argparse
import pathlib
import itertools


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


def _extract(file_path, dest_dir=None):
    ext = pathlib.Path(file_path).suffix
    if ext.endswith('.udp'):
        unpacker.unpack(file_path, dest_dir)
    elif ext.endswith('.LoxCC'):
        uncompress_loxcc(file_path, dest_dir)

def _sync_api_list(source):
    path = pathlib.Path(source)
    if path.exists():
        with open(source, 'r') as f:
            source = f.readlines()

    for cmd in [c.replace(',', '').strip() for c in source]:
        a = 5



def main():
    parser = argparse.ArgumentParser()
    extract_group = parser.add_argument_group()
    parser.add_argument('-a', '--analyze', help="Analyze the given configuration file. (Supported formats: .Loxone, .LoxCC)")
    extract_group.add_argument('-e', '--extract', metavar='FILE', type=argparse.FileType('rb'), help="Extract the given file. Specify the destination with the -d flag (Supports formats: .udp and .LoxCC")
    extract_group.add_argument('-d', '--dest-dir', metavar='PATH', help="Destination for the extracted resource")
    conn_grp = parser.add_argument_group()
    conn_grp.add_argument('-c', '--connect', help="establish a websocket connection to given Miniserver", action='store_true')
    conn_grp.add_argument('--host')
    conn_grp.add_argument('-p', '--port')
    parser.add_argument('--sync-api')

    args = parser.parse_args()
    if args.extract:
        _extract(args.extract, args.dest_dir)

    if args.connect:
        comm = LoxComm(args.host)
        # comm = LoxComm("demominiserver.loxone.com:7779")
        # comm.connect((user, password))
        # comm.check_api_fns(ALL_COMMANDS)
    if args.sync_api:
        _sync_api_list(args.sync_api)

# TODO check certificates
# TODO analyze UPD format
# TODO config file analyzer
# TODO test firewall capabilities


if __name__ == "__main__":
    main()

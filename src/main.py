from api import sync_api_list, check_api_fns
from comm import LoxComm, DummyComm
from api import sync_api_list, discover_api_fns
from update_analyzer import unpacker
from config_analyzer.loxcc_parser import uncompress_loxcc#, decompress_loxcc
import asyncio
import argparse
import pathlib


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


def _extract(file_path, dest_dir=None):
    ext = pathlib.Path(file_path).suffix
    if ext.endswith('.udp'):
        unpacker.unpack(file_path, dest_dir)
    elif ext.endswith('.LoxCC'):
        uncompress_loxcc(file_path, dest_dir)


def _get_line(source_file):
    source = []
    path = pathlib.Path(source_file)
    if path.exists():
        with open(path, 'r') as f:
            source = [c.replace(',', '').strip().strip('/') for c in f.readlines()]
    return source


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
    parser.add_argument('-u', '--user', help="User used to connect to the miniserver")
    parser.add_argument('--pwd', help="Password of the user")
    parser.add_argument('--sync-api', action='store_true')
    parser.add_argument('--discover-api', action='store_true')
    parser.add_argument('--input-file')
    parser.add_argument('--ms-version')

    args = parser.parse_args()
    if args.extract:
        _extract(args.extract, args.dest_dir)

    comm = None
    if args.connect:
        comm = LoxComm(args.host, args.user, args.pwd)
        # comm = LoxComm("demominiserver.loxone.com:7779")
        comm.connect()

    source = _get_line(args.input_file) if args.input_file else []
    if args.sync_api:
        new_cmds, unknown_cmds = sync_api_list(source, args.ms_version)

    if args.discover_api and comm:
        # check_api_fns(unknown_cmds, comm)
        discover_api_fns(source, comm)


# TODO check certificates
# TODO analyze UPD format
# TODO config file analyzer
# TODO test firewall capabilities


if __name__ == "__main__":
    main()

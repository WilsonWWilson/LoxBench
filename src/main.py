from comm import LoxComm, DummyComm
from secrets.credentials import user, password
from api import sync_api_list, discover_api_fns
from secrets.credentials import user, password
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


def _clean_command(cmd):
    return cmd.replace(',', '').strip('/').strip()


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
    parser.add_argument('--ms-version')

    args = parser.parse_args()
    if args.extract:
        _extract(args.extract, args.dest_dir)

    if args.connect:
        comm = LoxComm(args.host)
        # comm = LoxComm("demominiserver.loxone.com:7779")
        # comm.connect((user, password))
        # comm.check_api_fns(ALL_COMMANDS)
    if args.sync_api:
        source = []
        path = pathlib.Path(args.sync_api)
        if path.exists():
            with open(path, 'r') as f:
                source = [c.replace(',', '').strip().strip('/') for c in f.readlines()]
                # source = [_clean_command() for c in f.readlines()]
        # sync_api_list(args.sync_api, args.ms_version)

        if args.connect:
            comm = DummyComm()
            discover_api_fns(source, comm)

# TODO check certificates
# TODO analyze UPD format
# TODO config file analyzer
# TODO test firewall capabilities


if __name__ == "__main__":
    main()

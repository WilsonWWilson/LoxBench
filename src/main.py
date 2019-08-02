import statistics
from communication.comm import LoxComm
from api import sync_api_list, discover_api_fns
from firmware_analyzer import unpacker, binary_analyzer
from config_analyzer.loxcc_parser import uncompress_loxcc  # , decompress_loxcc
import argparse
import pathlib


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


def _extract(file_path, dest_dir=None):
    ext = pathlib.Path(file_path).suffix
    if ext.endswith('.upd'):
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


def analyzer(args):
    ext = pathlib.Path(args.input_file).suffix
    if ext in ['.bin', '.upd']:
        # TODO analyze UPD format
        binary_analyzer.analyze(args.input_file)
    elif ext in ['.Loxone', 'LoxCC']:
        # TODO config file analyzer
        raise NotImplementedError
    else:
        raise ValueError(f"'{args.input_file}' - unknown filetype")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='sub_cmds')
    analyze_parser = subparsers.add_parser('analyze', aliases=['a'], help="Analyze the given configuration file. (Supported formats: .Loxone, .LoxCC)")
    # parser.add_argument('-a', '--analyze',
    analyze_parser.add_argument('input_file')
    analyze_parser.set_defaults(func=analyzer)

    extract_group = parser.add_argument_group()
    extract_group.add_argument('-e', '--extract', metavar='FILE', help="Extract the given file. Specify the destination with the -d flag (Supports formats: .upd and .LoxCC")
    # extract_group.add_argument('-i', '--input-file', metavar='FILE', help="Extract the given file. Specify the destination with the -d flag (Supports formats: .upd and .LoxCC")
    extract_group.add_argument('-d', '--dest-dir', metavar='PATH', help="Destination for the extracted resource")

    conn_grp = parser.add_argument_group()
    conn_grp.add_argument('-c', '--connect', help="establish a websocket connection to given Miniserver", action='store_true')
    conn_grp.add_argument('--host')
    conn_grp.add_argument('-p', '--port')
    parser.add_argument('-u', '--user', help="User used to connect to the miniserver")
    parser.add_argument('--pwd', help="Password of the user")
    parser.add_argument('--sync-api', action='store_true')
    parser.add_argument('--discover-api', action='store_true')
    parser.add_argument('-i', '--input-file')
    parser.add_argument('--ms-version')

    args = parser.parse_args()

    if args.sub_cmds is None:
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
    else:
        args.func(args)  # call the sub-command handler set via 'set_defaults'


# TODO check certificates
# TODO test firewall capabilities
# TODO analyze Config connection ('wsx://' + credentials as Sec-WebSocket-Protocol)


if __name__ == "__main__":
    main()

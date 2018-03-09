from comm import LoxComm
from secrets.credentials import host, user, password
from update_analyzer import unpacker


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


def main():
    # unpacker.unpack('../samples/upd/09030225_Miniserver.upd')
    comm = LoxComm(host)
    comm.connect((user, password))

# TODO check certificates
# TODO analyze UPD format
# TODO config file unpacker (LoxCC)
# TODO config file analyzer


if __name__ == "__main__":
    main()
